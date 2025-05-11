# 8-puzzle-ai


1/CÁC THUẬT TOÁN TÌM KIẾM CÓ THÔNG TIN (INNFORMED SEARCH)

Các thuật toán này sử dụng một hàm heuristic h(n) để ước lượng chi phí từ trạng thái hiện tại n đến trạng thái đích. Heuristic này cung cấp "thông tin" về đích đến, giúp hướng dẫn tìm kiếm hiệu quả hơn so với tìm kiếm mù quáng. Trong dự án này, heuristic chính được sử dụng là Khoảng cách Manhattan: h(n) là tổng khoảng cách (tính theo số ô di chuyển ngang và dọc) mà mỗi ô số (từ 1 đến 8) phải di chuyển từ vị trí hiện tại của nó trong trạng thái n để về đúng vị trí trong trạng thái đích.

Thuật toán A*:

Ý tưởng: 

Thuật toán A* sử dụng công thức đánh giá: f(n) = g (n) + h(n) với g(n) là chi phí từ điểm bắt đầu đến nút n; h(n) là àm heuristic - ước lượng chi phí còn lại từ n đến đích. Thuật toán luôn chọn nút có giá trị f(n) nhỏ nhất trong hàng đợi ưu tiên để mở rộng tiếp

Nhận xét:

Tính tối ưu: A* đảm bảo tìm ra đường đi tối ưu nếu hàm heuristic h(n) là chấp nhận được (admissible), nghĩa là h(n) không bao giờ đánh giá quá cao chi phí thực tế để đạt đích (luôn ≤ chi phí thực tế). Khoảng cách Manhattan là một heuristic chấp nhận được cho 8-puzzle. Tính tối ưu cũng đòi hỏi h(n) nhất quán (consistent) hoặc có kiểm tra trạng thái đã thăm khi một nút được tìm thấy lại qua đường đi tốt hơn.

Tính đầy đủ: Có.

Độ phức tạp thời gian: Phụ thuộc mạnh vào chất lượng của heuristic. Với heuristic tốt, A* có thể hiệu quả hơn nhiều so với các thuật toán không thông tin. Trong trường hợp xấu nhất, nó có thể suy biến thành BFS/UCS.

Độ phức tạp không gian (bộ nhớ): Vẫn có thể rất lớn. A* lưu trữ tất cả các nút đã được sinh ra trong bộ nhớ (trong hàng đợi ưu tiên và danh sách đóng). Đây là hạn chế chính của A*.

![ScreenRecording2025-05-11235627-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/123bc6ed-9e20-4e97-9bca-d5549a3fad90)







Thuật toán Greedy:


Ý tưởng: 

Đây là thuật toán chỉ quan tâm đến hàm heuristic h(n)- tức là nó luôn chọn các trạng thái mà nó tin là gần đích nhất mà không xét đến chi phí đã đi và sử dụng hàng đợi ưu tiên dựa trên h(n):    
                                                                        f(n) = h(n)


Nhận xét:

Tính tối ưu: Vì bỏ qua g(n), nó có thể đi vào một đường dài mặc dù có vẻ gần đích ở mỗi bước.

Tính đầy đủ: Có thể đi vào vòng lặp nếu không kiểm tra trạng thái đã thăm. Nó cũng có thể bị kẹt và không tìm thấy lời giải ngay cả khi nó tồn tại.

Độ phức tạp thời gian: Thường nhanh hơn A* hoặc BFS để tìm ra một lời giải (không nhất thiết tối ưu), độ phức tạp trong trường hợp xấu nhất là O(b^m).

Độ phức tạp không gian: Thường ít hơn A* nhưng trong trường hợp xấu nhất cũng là O(b^m).

![ScreenRecording2025-05-12001310-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2c423500-153c-4f6b-9fa1-ea5fa25f07be)




Thuật toán IDA*:

Ý tưởng: 

Đây là thuật toán kết hợp giữ A* và IDDFS (duyệt theo chiều sâu có giới hạn, tăng dần giới hạn). Mục đích nhằm tìm đường tối ưu như A* nhưng tiết kiệm bộ nhớ hơn.
Cách hoạt động:

Chúng ta bắt đầu với bound = h(start): chính là chi phí dự tính từ trạng thái ban đầu đến đích

Tiếp tục duyệt theo chiều sâu nếu f(n) > h(start):
            
            nếu đến đích thì trả về kết quả

            nếu chưa đến đích thì ghi nhận các f(n) đã vượt ngưỡng và chọn ngưỡng nhỏ nhất trong số đó làm bound mới

Nhận xét: 

Tính tối ưu: Có (với heuristic chấp nhận được, giống A*).

Tính đầy đủ: Có.

Độ phức tạp thời gian: Tương tự A* về mặt lý thuyết, nhưng có thể chậm hơn trong thực tế do phải duyệt lại các nút ở các lần lặp trước. Tuy nhiên, nếu số lượng nút tăng mạnh theo giá trị f, chi phí duyệt lại không quá lớn.

Độ phức tạp không gian (bộ nhớ): O(bd). Giống như IDDFS, IDA chỉ yêu cầu bộ nhớ tuyến tính theo độ sâu của lời giải. Đây là ưu điểm vượt trội so với A* cho các bài toán có không gian trạng thái rất lớn.


![ScreenRecording2025-05-12002209-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/94754449-3044-4b07-863d-364bcb495597)



2/CÁC THUẬT TOÁN TÌM KIẾM KHÔNG THÔNG TIN (UNINFORMED SEARCH):



