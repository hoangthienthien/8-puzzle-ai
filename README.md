# 8-puzzle-ai

Thuật toán A*:
Ý tưởng: 
Thuật toán A* sử dụng công thức đánh giá: f(n) = g (n) + h(n) với g(n) là chi phí từ điểm bắt đầu đến nút n; h(n) là àm heuristic - ước lượng chi phí còn lại từ n đến đích. Thuật toán luôn chọn nút có giá trị f(n) nhỏ nhất trong hàng đợi ưu tiên để mở rộng tiếp
Nhận xét:
Tính tối ưu: A* đảm bảo tìm ra đường đi tối ưu nếu hàm heuristic h(n) là chấp nhận được (admissible), nghĩa là h(n) không bao giờ đánh giá quá cao chi phí thực tế để đạt đích (luôn ≤ chi phí thực tế). Khoảng cách Manhattan là một heuristic chấp nhận được cho 8-puzzle. Tính tối ưu cũng đòi hỏi h(n) nhất quán (consistent) hoặc có kiểm tra trạng thái đã thăm khi một nút được tìm thấy lại qua đường đi tốt hơn.
Tính đầy đủ: Có.
Độ phức tạp thời gian: Phụ thuộc mạnh vào chất lượng của heuristic. Với heuristic tốt, A* có thể hiệu quả hơn nhiều so với các thuật toán không thông tin. Trong trường hợp xấu nhất, nó có thể suy biến thành BFS/UCS.
Độ phức tạp không gian (bộ nhớ): Vẫn có thể rất lớn. A* lưu trữ tất cả các nút đã được sinh ra trong bộ nhớ (trong hàng đợi ưu tiên và danh sách đóng). Đây là hạn chế chính của A*.

![ScreenRecording2025-05-11235627-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/123bc6ed-9e20-4e97-9bca-d5549a3fad90)
thuật toán Greedy:
Ý tưởng: Đây là thuật toán chỉ quan tâm đến hàm heuristic h(n)- tức là nó luôn chọn các trạng thái mà nó tin là gần đích nhất mà không xét đến chi phí đã đi và sử dụng hàng đợi ưu tiên dựa trên h(n):    f(n) = h(n)
Nhận xét:
Tính tối ưu: Vì bỏ qua g(n), nó có thể đi vào một đường dài mặc dù có vẻ gần đích ở mỗi bước.
Tính đầy đủ: Có thể đi vào vòng lặp nếu không kiểm tra trạng thái đã thăm. Nó cũng có thể bị kẹt và không tìm thấy lời giải ngay cả khi nó tồn tại.
Độ phức tạp thời gian: Thường nhanh hơn A* hoặc BFS để tìm ra một lời giải (không nhất thiết tối ưu), độ phức tạp trong trường hợp xấu nhất là O(b^m).
Độ phức tạp không gian: Thường ít hơn A* nhưng trong trường hợp xấu nhất cũng là O(b^m).

![ScreenRecording2025-05-12001310-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2c423500-153c-4f6b-9fa1-ea5fa25f07be)
