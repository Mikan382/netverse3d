# Hệ thiết kế giao diện

Giao diện 2D dùng Saigon Soft-Future theo [ADR-0040](../../decisions/ADR-0040-saigon-soft-future-ui.md). Khi thêm giao diện, đối chiếu [tiêu chí kiểm duyệt](../product/ui-criteria.md) và [ranh giới lớp của client](./web-client.md).

## Token

| Tầng       | Ví dụ                                                   | Quy tắc                                                                                      |
| ---------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Gốc        | Bảng màu, thang cỡ chữ và khoảng cách                   | Giá trị đặt ở `packages/ui/tokens/primitive.css`.                                            |
| Ngữ nghĩa  | `--ui-surface`, `--ui-text`, `--ui-focus`, `--ui-error` | Đặt tên theo vai trò trong `packages/ui/tokens/semantic.css`. Màu tiệm đi qua `--ui-accent`. |
| Thành phần | Mặt nền, viền, khoảng cách của nút và hộp thoại         | Đặt cạnh component. Mỗi biến tham chiếu token ngữ nghĩa phù hợp.                             |

Thời lượng chuyển động nằm ở `packages/ui/tokens/motion.css`. Token mặt nền cung cấp biến thể đặc cho panel kính. `apps/web-3d` truyền mức chất lượng từ trạng thái cảnh sang UI.

## Thêm một thành phần

1. Tìm component có vai trò và trạng thái tương đương trong `packages/ui`.
2. Nếu cần thêm, viết component và kiểu bên cạnh nhau. Dùng token ngữ nghĩa và nhãn tiếng Việt của màn hình gọi.
3. Giữ trạng thái thao tác theo ADR-0040. App cập nhật trạng thái từ phòng hoặc API.
4. Thêm mẫu của mọi biến thể và trạng thái vào thư viện, kèm mã tiêu chí giao diện.
5. Chạy bộ test và kiểm bố cục, phím, chạm, focus ở mức chất lượng thấp lẫn cao.

## Thư viện

[Thư viện giao diện](https://netverse3d.github.io/netverse3d/ui/) bắt đầu từ [#417](https://github.com/netverse3d/netverse3d/issues/417). Mục Nền tảng cho xem token, tương phản và các tuỳ chọn. Mục Component trình bày biến thể và trạng thái. Mục Mẫu tương tác diễn lại luồng từ thao tác đến phản hồi và khôi phục.
