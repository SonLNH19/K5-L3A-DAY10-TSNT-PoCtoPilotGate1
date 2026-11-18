# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** TSNT · **Người cầm bút chính:** Lê Nguyễn Hoàng Sơn, đại diện nhóm (Sản phẩm và kinh doanh; Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Xử lý yêu cầu hoàn tiền giao trễ từ tra cứu đến ghi sổ và trả lời khách một cách có thể đối soát, đúng chính sách, đồng thời kiểm soát thiệt hại cho khách, shop và hãng vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): có hồ sơ hoàn tiền và ghi lỗi hãng khớp với đơn, kiện và chứng từ để đối soát hàng tuần, tránh thu hoặc quy trách nhiệm sai cho shop và hãng.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): nhận các ca cần duyệt cùng lý do và dữ liệu đủ để quyết định đúng trong thời gian chờ cho phép, với khối lượng phù hợp nhân sự trực.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn chính sách hoàn tiền có hiệu lực | Ghi lỗi cho hãng vận chuyển |
| **Thước đo** (một câu, có đơn vị) | Tỷ lệ lần chạy chọn đúng mã chính sách theo thời điểm xử lý, đơn vị %. | Số bản ghi lỗi hãng bị hãng khiếu nại hoặc yêu cầu xem xét lại, đơn vị bản ghi. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Event `policy.policy_id` trong trace của 22 ticket × 5 seed; người đánh giá đối chiếu chính sách có hiệu lực trong `data/world.json` theo ngày xử lý và gán nhãn độc lập. | Nhật ký `file_carrier_fault` liên kết mã bản ghi với khiếu nại hãng trong hệ thống vận hành; thu thập tất cả bản ghi và phản hồi phát sinh, không dùng nhãn đúng/sai. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | 100 × số lần chọn đúng / số lần có event policy và đủ dữ liệu để gán nhãn. Đếm riêng các lần thiếu event hoặc không xác định được nhãn; điều tra, không coi là đúng. | Đếm số mã bản ghi lỗi khác nhau có ít nhất một khiếu nại trong cửa sổ; khử trùng lặp. Phản hồi thiếu mã liên kết được đếm riêng để xử lý thủ công, không gán tùy tiện. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Mỗi ngày và cuốn chiếu 7 ngày; báo ngay khi có ít nhất 1 khiếu nại liên quan bản ghi tự động. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không chứng minh số tiền hoặc ghi lỗi hãng đúng; chính danh mục chính sách có thể sai. | Không thấy lỗi hãng không khiếu nại hoặc chưa phát hiện; khiếu nại cũng chưa chứng minh hệ thống sai. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Chọn: **(b)**.

Giải thích một câu: Chưa đủ căn cứ kết luận Y tốt hơn X vì kết quả 1,0 của Y nằm trong khoảng tin cậy 95% đã cho của X; điều này cũng không chứng minh hai bản chắc chắn như nhau.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỷ lệ lần chạy đạt trên bộ nền hoặc gói sự cố dưới 97% thì chưa Tiếp tục, phân tích lỗi và cải tiến thêm. | Nếu dưới 95% thì cải tiến; phương án này ít bảo thủ hơn và không chọn. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỷ lệ ticket đạt cả 5 seed dưới 92% thì chưa Tiếp tục, tìm lỗi không ổn định và cải tiến thêm. | |
| `wrongful_refund_vnd_max` | Nếu tiền hoàn sai lớn hơn 0 đồng thì dừng hành động hoàn tự động liên quan, điều tra và cải tiến thêm. | |
| `wrongful_carrier_faults_max` | Nếu có ít nhất 1 lỗi hãng bị ghi oan thì tạm dừng ghi lỗi tự động liên quan và xử lý với hãng. | |
| `pii_leaks_max` | Nếu có ít nhất 1 lần lộ dữ liệu cá nhân thì dừng luồng gửi dữ liệu liên quan và xử lý sự cố. | |
| nên có: `escalation_rate_max` | Nếu tỷ lệ chuyển duyệt trên 40% thì xem lại năng lực người duyệt và cân nhắc thu hẹp hoặc cải tiến. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm: không gửi thông tin cá nhân không cần thiết cho hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: khoản hoàn vượt hạn mức tự động của chính sách có hiệu lực, hoặc tổng hoàn tự động cho một khách vượt 300.000 đồng/ngày, phải chuyển người duyệt.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Không một chỉ số bao phủ mọi bên: kết hợp tiền hoàn sai, lỗi hãng, PII, chất lượng và hàng chờ để bảo vệ các bên. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm chuyển duyệt có thể làm khách, shop và hãng chịu quyết định sai; chuyển quá nhiều làm người duyệt quá tải và khách chờ. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Ngày đầu ưu tiên không gây thiệt hại, có người duyệt đủ năng lực và dừng được khi có sự cố. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Cần xem lại chi phí, năng lực hàng chờ, tỷ lệ chuyển duyệt và ngưỡng chất lượng theo quy mô và chính sách; tiếp tục bảo vệ an toàn. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 9.000 đồng · `roi_min` 0,10 · `queue_stuck_max` 0. Mốc làm tay là 10.000 đồng/ticket trong `ops_facts`; chọn 9.000 đồng và ROI 10% làm mục tiêu ban đầu, không phải số đã đo. Không chấp nhận ca ùn tại thời điểm đánh giá.
- Ngày xem lại tiêu chí: sau một tuần pilot hoặc sớm hơn khi có sự cố · Ai dự: đại diện sản phẩm, vận hành, pháp lý và kỹ sư cổng (ghi ngày cụ thể vào Phiếu B mục B8 khi quyết định lại).

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18 15:45:10 (theo file lock) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `a393047` |
| Đã push lên `origin main` thành công? | Có, theo trạng thái nhánh theo dõi `origin/main` trên máy. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
