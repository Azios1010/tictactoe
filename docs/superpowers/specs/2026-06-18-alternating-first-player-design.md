# Thiết kế luân phiên người đi trước

## Mục tiêu

Trong chế độ Play, quyền đi trước đổi sau mỗi lần người dùng bấm **New game**:

- Ván đầu tiên: người chơi (`-1`, X) đi trước.
- Ván thứ hai: AI (`1`, O) đi trước.
- Các ván tiếp theo tiếp tục luân phiên.

Arena mode không bị ảnh hưởng.

## Thiết kế

Frontend giữ một state xác định bên đi trước của ván hiện tại. `resetPlayMode` nhận bên đi trước cho ván mới, dọn toàn bộ trạng thái ván cũ, rồi:

- Nếu người chơi đi trước, hiển thị trạng thái chờ người chơi.
- Nếu AI đi trước, khóa bàn cờ và gọi endpoint `POST /api/get-move` với board rỗng.

Backend đã hỗ trợ board rỗng và trả về nước `opening_center`, vì vậy không cần thay đổi AI core hoặc API.

Nút **New game** đảo bên đi trước hiện tại trước khi reset. Khi chuyển từ Arena về Play, chuỗi luân phiên được khởi tạo lại với người chơi đi trước để hành vi dễ dự đoán.

## Luồng dữ liệu

1. Ứng dụng mở ở Play mode với người chơi đi trước.
2. Người dùng bấm **New game**.
3. Frontend đảo bên đi trước sang AI, tạo board rỗng và gọi `requestAiMove`.
4. Trong lúc chờ backend, bàn cờ bị khóa bởi `isThinking`.
5. AI đặt quân `1`; sau đó người chơi có thể click.
6. Lần bấm **New game** tiếp theo đảo lại sang người chơi.

## Xử lý lỗi

Nếu backend không phản hồi khi AI phải đi trước, board vẫn rỗng và thông báo lỗi hiện có được hiển thị. Người chơi không được tự đặt quân trong lúc request đang chạy; sau khi request thất bại, người dùng có thể bấm **New game** để chuyển sang ván kế tiếp.

## Kiểm thử

- Tách logic xác định bên đi trước kế tiếp thành helper thuần để kiểm thử.
- Kiểm tra chuỗi người → AI → người.
- Build frontend để phát hiện lỗi JSX hoặc import.
- Kiểm tra thủ công rằng backend nhận board rỗng và AI trả `opening_center` đã được bao phủ bởi hành vi hiện có của AI core.

## Phạm vi

Không đổi quy ước quân cờ, difficulty, backend API, AI search hoặc Arena mode. Không thêm tùy chọn chọn bên đi trước thủ công.
