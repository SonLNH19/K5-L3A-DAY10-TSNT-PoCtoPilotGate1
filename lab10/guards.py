"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("Không xác định được chính sách có hiệu lực")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool in ("issue_refund", "file_carrier_fault"):
        if any(event.get("type") == "model_override" and event.get("field") == "delay_days"
               and event.get("db") != event.get("ticket") for event in ctx.events):
            return Verdict.escalate("Ngày trễ trong ticket khác tracking; cần người xác minh")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if not order or not order.get("parcels") or policy is None:
            return Verdict.escalate("Thiếu dữ liệu để xác minh quyền lợi trước khi hoàn")
        if (ctx.ticket.get("parcel_id") and not any(
                p.get("parcel_id") == ctx.ticket["parcel_id"] for p in order["parcels"])):
            return Verdict.escalate("Không tìm thấy kiện yêu cầu hoàn trong đơn")
        try:
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            if not parcel.get("delay_cause"):
                return Verdict.escalate("Chưa có nguyên nhân trễ để xác minh quyền lợi")
            delay = H.db_delay_days(parcel, ctx.as_of)
            entitlement = H.entitlement_vnd(policy, order, delay, parcel["delay_cause"])
            paid = sum(row["amount_vnd"] for row in
                       ctx.tools.ledger_rows(order_id=order["order_id"]))
            remaining = max(0, entitlement - paid)
            amount = action.get("amount_vnd")
            if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
                return Verdict.escalate("Số tiền hoàn không hợp lệ")
        except (KeyError, TypeError, ValueError):
            return Verdict.escalate("Dữ liệu quyền lợi không đủ hoặc không hợp lệ")
        if amount > remaining:
            return Verdict.escalate("Khoản hoàn vượt quyền lợi còn lại theo tracking và chính sách")

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        parcel = next((p for p in (order or {}).get("parcels", [])
                       if p.get("parcel_id") == action.get("parcel_id")), None)
        if not parcel or not policy or not parcel.get("promised_date"):
            return Verdict.escalate("Thiếu thông tin kiện hoặc chính sách để ghi lỗi hãng")
        delay = H.db_delay_days(parcel, ctx.as_of)
        if (action.get("carrier_id") != parcel.get("carrier_id")
                or action.get("delay_days") != delay
                or not H.carrier_at_fault(policy, parcel, delay)):
            return Verdict.deny("Không ghi lỗi hãng khi không khớp tracking và chính sách")
    return Verdict.allow()
