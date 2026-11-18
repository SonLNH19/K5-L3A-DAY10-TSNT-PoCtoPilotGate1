# Team

## Thông tin nhóm

- Tên nhóm: `TSNT`:
- Lớp: `L3A` 
- Repo của bàn: `K5-L3A-DAY10-TSNT-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):S4

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |Nguyễn Mạnh Tường          |2A202603646      |Kỹ sư cổng     |             |
|   2 |Lê Nguyễn Hoàng Sơn           |2A202603686      |Sản phẩm và kinh doanh     | Trưởng nhóm            |
|   3 |Vũ Thành Toàn           |2A202603654      |Vận hành và pháp lý     |             |
|   4 |Phạm Văn Nam           |2A202603681      |Kỹ sư cổng       |           |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenManhTuong-2A202603646

### Phần việc phụ trách

Rà soát câu 2.6 và 3.5, Phiếu B mục B7.1 và Phiếu C mục C7; tập trung vào `lab10/guards.py`.

### Đóng góp cụ thể
Phần cổng vòng 1 trong commit chung 80bfdf9
Rà soát cổng kiểm tra quyền lợi trước khi hoàn tiền. Đối chiếu số ngày trễ trong tracking với đề xuất hoàn và kiểm tra cách chuyển người duyệt khi thiếu dữ liệu hoặc số tiền vượt quyền lợi còn lại.

### Bằng chứng

Phiếu C mục C2 và C7; trace `S4-05@11`; lần chạy `R-S4-after-20261118-164526-7b9798` có tiền hoàn sai bằng 0.

### Sử dụng AI

Dùng AI hỗ trợ giải thích luồng xử lý, gợi ý cách kiểm tra quyền lợi và soát nội dung phân tích.

### Exit ticket

- Học được cách kiểm tra điều kiện trước khi hoàn tiền, tránh chặn quá muộn khi tiền đã ghi vào sổ.
- Chưa rõ cách xử lý khi dữ liệu tracking bị sai hoặc cập nhật chậm.


## LeNguyenHoangSon-2A202603686

### Phần việc phụ trách

Trưởng nhóm, sản phẩm và kinh doanh; Phiếu A, Phiếu B mục B8 và Phiếu C mục C12; rà soát tiêu chí, chi phí, ngân sách và hồ sơ nộp bài.

### Đóng góp cụ thể

Tổng hợp tiêu chí chấp nhận và thực hiện các lệnh trên máy chung. Đối chiếu kết quả với ngưỡng đã ký, theo dõi chi phí và ROI, tổng hợp quyết định v1/v2 và kiểm tra thành phần bài nộp.

### Bằng chứng

Trực tiếp ký và push tiêu chí tại commit a393047; commit, push cổng vòng 1 tại 80bfdf9; thực hiện các lệnh đánh giá và gom bài. Report cuối: R-S4-grade-20261118-172326-7ee168.

### Sử dụng AI

Dùng AI hỗ trợ đọc hướng dẫn, đề xuất cách viết cổng, soạn thảo các phiếu và kiểm tra lỗi. Các lệnh đánh giá được chạy trên máy để lấy số liệu thực tế.

### Exit ticket

- Hiểu rằng xử lý đúng ticket chưa đủ, còn phải cân đối ngân sách, chi phí và khả năng duyệt của nhân viên.
- Chưa rõ chi phí và ROI sẽ thay đổi bao nhiêu khi chuyển từ dữ liệu giả sang vận hành thật.


## VuThanhToan-2A202603654

### Phần việc phụ trách

Vận hành và pháp lý; rà soát câu 2.4, 2.10 và phần cập nhật sau sự cố; Phiếu B mục B4–B5, B7.5–B7.6 và Phiếu C mục C10–C11.

### Đóng góp cụ thể

Rà soát hàng chờ, thời gian chờ và kế hoạch nhân sự duyệt. Đối chiếu cấu hình với runbook, kiểm tra điều kiện cảnh báo, dừng thao tác và các rủi ro đối với hãng vận chuyển, khách hàng và người duyệt.

### Bằng chứng
Cấu hình vận hành trong commit chung 80bfdf9

`config/operating_gates.json`; Phiếu C mục C10–C11; lần chạy `R-S4-after-20261118-165016-44ef7f` có 2 người duyệt, thời gian chờ tối đa 23 phút và 0 ca bị ùn.

### Sử dụng AI

Dùng AI hỗ trợ giải thích số liệu hàng chờ, gợi ý cách trình bày runbook và soát các tình huống vận hành.

### Exit ticket

- Nhận ra chuyển nhiều ca sang người duyệt có thể làm hàng chờ quá tải dù từng ticket được xử lý đúng.
- Chưa chắc hai người duyệt có duy trì được công suất 12 ca mỗi giờ vào lúc cao điểm không.


## PhamVanNam-2A202603681

### Phần việc phụ trách

Kỹ sư cổng; rà soát cổng ghi lỗi hãng, chỉ số theo dõi và kết quả kiểm thử; Phiếu C mục C7–C8, `lab10/guards.py` và `lab10/monitors.py`.

### Đóng góp cụ thể

Rà soát cách từ chối riêng lệnh ghi lỗi hãng không hợp lệ để tránh chuyển duyệt sau khoản hoàn đúng. Kiểm tra ý nghĩa của chỉ số `policy_fallback_rate` và đối chiếu kết quả S4 với bộ nền để nhận biết hồi quy.

### Bằng chứng

Nội dung kiểm thử vòng 1 trong commit chung 80bfdf9; Trace `S4-08@11` và `S4-08@22`; Phiếu C mục C7–C8; report `R-S4-grade-20261118-172326-7ee168` có `visible`, `regression` và `monitor` đều đạt.

### Sử dụng AI

Dùng AI hỗ trợ giải thích trace, công thức monitor và cách đọc report; đối chiếu các nhận xét với kết quả chạy thực tế.

### Exit ticket

- Hiểu thêm cách dùng monitor để phát hiện LLM chuyển sang fallback, kể cả khi chưa gây hoàn tiền sai.
- Chưa chắc các cổng hiện tại có xử lý được hết những trường hợp trong test ẩn không.