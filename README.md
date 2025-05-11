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

Thuật toán BFS:
Ý tưởng: 
Mở rộng nút nnoong nhất chưa được mở rộng, tức là thuật toán sẽ duyệt toàn bộ các nút ở độ sâu k trước khi duyệt bất kỳ nút nào ở độ sâu k+1. Thuật toán sử dụng hàng đợi (Queue) và tuân thoe nguyên tắc FIFO.

Nhận xét:
Tính tối ưu: BFS đảm bảo tìm ra đường đi ngắn nhất (ít bước di chuyển nhất) vì nó luôn tìm thấy nút đích nông nhất trước.

Tính đầy đủ: Nếu có lời giải tồn tại, BFS chắc chắn sẽ tìm thấy nó.

Độ phức tạp thời gian: O(b^d), trong đó b là nhân tố nhánh (số hành động tối đa từ một trạng thái, tối đa là 4) và d là độ sâu của lời giải nông nhất. Có thể rất chậm nếu lời giải ở sâu.

Độ phức tạp không gian (bộ nhớ): O(b^d). BFS phải lưu trữ tất cả các nút ở biên giới tìm kiếm trong hàng đợi và các nút đã thăm. Đây là hạn chế lớn nhất của BFS, có thể nhanh chóng cạn kiệt bộ nhớ.

![ScreenRecording2025-05-12001310-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/f603f97a-6707-433c-b4c8-ec1b8fae3679)

Thuật toán DFS:

Ý tưởng: Mở rộng nút sâu nhất có thể trước nghĩa là đi theo một nhánh cho tới tận cùng, chỉ quay lại khi gặp ngõ cụt hoặc đạt độ sâu giới hạn. Sử dụng ngăn xép (Stack) hoặc đệ quy và hoạt động theo nguyên tắc LIFO.

Nhận xét:

Tính tối ưu: DFS không đảm bảo tìm ra đường đi ngắn nhất. Nó có thể tìm thấy một lời giải rất dài trước khi tìm thấy lời giải ngắn hơn (nếu có) ở nhánh khác.

Tính đầy đủ: Nếu không giới hạn độ sâu và không kiểm tra trạng thái đã thăm, nó có thể bị kẹt trong vòng lặp.

Độ phức tạp thời gian: O(b^m), với m là độ sâu tối đa của không gian trạng thái (hoặc giới hạn độ sâu). Có thể nhanh hơn BFS nếu may mắn tìm thấy lời giải sớm, nhưng cũng có thể chậm hơn nhiều nếu lời giải nằm ở nhánh khác hoặc m lớn hơn d rất nhiều.

Độ phức tạp không gian (bộ nhớ): O(b*m). Yêu cầu bộ nhớ thấp hơn nhiều so với BFS, chỉ cần lưu trữ đường đi hiện tại và các nút chưa khám phá dọc theo đường đi đó. Đây là ưu điểm chính của DFS.


![ScreenRecording2025-05-12005142-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/352e9d86-4f43-400b-a529-2ade0e9385cc)


Thuật toán IDDFS:

Ý tưởng:

Mở rộng nút theo kiểu DFS có giới hạn độ sâu, nhưng lặp lại nhiều lần, mỗi lần tăng độ sâu giới hạn thêm 1. Thuật toán dựa trên DFS với depth_limit với độ sâu tăng lên 1 sau mỗi lần lặp.

Nhận xét:

Tính tối ưu: Giống như BFS, nó sẽ tìm thấy lời giải nông nhất đầu tiên.

Tính đầy đủ: Giống như BFS.

Độ phức tạp thời gian: O(b^d). Mặc dù có vẻ lãng phí khi duyệt lại các nút ở tầng trên nhiều lần, nhưng số nút ở tầng cuối (tầng d) thường chiếm phần lớn tổng số nút, nên chi phí duyệt lại không quá đáng kể so với BFS.

Độ phức tạp không gian (bộ nhớ): O(b*d). Giống như DFS, yêu cầu bộ nhớ thấp. IDDFS thường là thuật toán tìm kiếm không thông tin được ưa chuộng khi không gian tìm kiếm lớn và độ sâu lời giải không xác định.




![ScreenRecording2025-05-12010025-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d8e17145-1e55-49de-bd4e-d5543baaf494)

Thuật toán UCS:

Ý tưởng: Mở rộng nút có tổng chi phí đường đi nhỏ nhất (g(n)) từ gốc đến hiện tại. Tức là không quan tâm đến độ sâu hay heuristic mà chỉ quan tâm đến chi phí tích lũy thực tế. Thuật toán sử dụng hàng đợi ưu tiên với khóa g(n) (là chi phí góc đến trạng thái n).

Nhận xét:

Tính tối ưu: UCS đảm bảo tìm ra đường đi có tổng chi phí thấp nhất. Khi chi phí mỗi bước là như nhau và dương (ví dụ, bằng 1 như trong 8-puzzle), UCS hoạt động giống hệt BFS và tìm ra đường đi ngắn nhất.

Tính đầy đủ: Có (miễn là chi phí mỗi bước lớn hơn một hằng số dương nhỏ ε).

Độ phức tạp thời gian: O(b^(1 + floor(C*/ε))), trong đó C* là chi phí của lời giải tối ưu. Khi chi phí bước là 1 (ε=1) và C*=d, độ phức tạp trở thành O(bd+1) hoặc O(bd) tùy cách cài đặt, tương đương BFS.

Độ phức tạp không gian (bộ nhớ): O(b^(1 + floor(C*/ε))). Tương tự BFS, UCS thường yêu cầu bộ nhớ rất lớn vì phải lưu trữ nhiều nút trong hàng đợi ưu tiên.


![ScreenRecording2025-05-12011230-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/deec5dd7-776e-4758-ba54-08a209aa624e)

3/ CÁC THUẬT TOÁN TÌM KIẾM CỤC BỘ (LOCAL SEARCH)

Thuật toán leo đồi đơn giản (Simple hill climbing):

Ý tưởng: Tìm lời giải bằng cách luôn di chuyển sang trạng thái hàng xóm có heuristic h(n) tốt hơn (nhỏ hơn). Sử dụng lệnh lặp While với 1 trạng thái hiện tại

Nhận xét:

Tính tối ưu/Đầy đủ: Thuật toán rất dễ bị "mắc kẹt" tại:
      
      Cực tiểu địa phương (Local Minimum): Một trạng thái tốt hơn tất cả các hàng xóm của nó nhưng không phải là tốt nhất toàn cục (trạng thái đích).
      
      Bình nguyên (Plateau): Một vùng không gian trạng thái phẳng nơi các hàng xóm có cùng giá trị heuristic, khiến thuật toán không biết đi đâu.
      
      Sườn núi (Ridge): Một khu vực khó di chuyển lên theo hướng tối ưu.

Độ phức tạp thời gian: nhanh ở mỗi bước. Tùy thuộc vào có dễ bị kẹt ở các bình nguyên không.

Độ phức tạp không gian (bộ nhớ): O(1). Chỉ cần lưu trữ trạng thái hiện tại.

![ScreenRecording2025-05-12014441-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/dbab5409-e11e-436a-8ab1-d586cbaf1cab)


Thuật toán leo đồi dốc nhất (Steepest Ascent Hill Climbing):

Ý tưởng:

Tương tự Hill-Climbing, nhưng xét toàn bộ hàng xóm và chọn hàng xóm tốt nhất, tức có 
h(n) nhỏ nhất, rồi di chuyển đến đó nếu tốt hơn.
→ Giống như leo xuống đoạn dốc nhanh nhất trong mọi hướng.
 Nhận xét:

Tính tối ưu: Vẫn có thể bị kẹt ở cực tiểu địa phương, bình nguyên, sườn núi

Độ phức tạp thời gian: Chậm hơn Simple HC ở mỗi bước vì phải đánh giá tất cả các trạng thái lan cận mới chọn ra được trạng thái có h(n) ngắn nhất

Độ phức tạp không gian (bộ nhớ): O(1).

![ScreenRecording2025-05-12015319-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/e9d3f0a5-6f54-460d-8aee-e2834628ac80)


Thuật toán leo đồi ngẫu nhiên (Stochastic Hill Climbing):

Ý tưởng:

Giống Steepest-Ascent, nhưng thay vì chọn hàng xóm tốt nhất, thuật toán xáo trộn tất cả hàng xóm và di chuyển ngay khi thấy một hàng xóm tốt hơn hiện tại.
→ Tăng tính ngẫu nhiên, giúp thoát bẫy đỉnh cục bộ tốt hơn.

Nhận xét:

Tính tối ưu/Đầy đủ: Vẫn có thể bị kẹt, nhưng tính ngẫu nhiên có thể giúp khám phá các phần khác nhau của sườn dốc.

Độ phức tạp thời gian: Tốc độ thay đổi tùy thuộc vào việc chọn ngẫu nhiên.

Độ phức tạp không gian (bộ nhớ): O(1).



![ScreenRecording2025-05-12020120-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/3f6ea079-7922-4539-a088-8c96b2335580)


Thuật toán Simulated Annealing

Ý tưởng:
Là một thuật toán leo đồi ngẫu nhiên có khả năng thoát khỏi cực tiểu địa phương. Nó cho phép di chuyển đến trạng thái xấu hơn (heuristic cao hơn) với một xác suất nhất định. Xác suất này (P = exp(-ΔE/T)) phụ thuộc vào mức độ xấu đi (ΔE = h(next) - h(current) > 0) và một tham số "nhiệt độ" (T). Ban đầu, T cao, cho phép di chuyển xấu nhiều hơn (khám phá rộng). Dần dần, T giảm theo một "lịch trình làm nguội" (cooling schedule), khiến xác suất chấp nhận nước đi xấu giảm xuống, thuật toán trở nên "tham lam" hơn (khai thác).

Nhận xét:

Tính tối ưu: có khả năng tìm được lời giải tốt hơn đáng kể so với các phiên bản Hill Climbing đơn giản do khả năng thoát khỏi cực tiểu địa phương.

Độ phức tạp thời gian: Thường chậm hơn Hill Climbing do có thể khám phá nhiều trạng thái hơn và cần tính toán xác suất. Hiệu suất phụ thuộc nhiều vào lịch trình làm nguội.

Độ phức tạp không gian (bộ nhớ): O(1).



![ScreenRecording2025-05-12020720-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/fc04f36e-c149-4bbb-873f-99b4b50fc686)

Thuật toán Di truyền (Genetic Algorithm)

Ý tưởng:
Là một thuật toán tìm kiếm dựa trên quần thể, mô phỏng quá trình chọn lọc tự nhiên và di truyền. Nó duy trì một tập hợp (quần thể - population) các trạng thái (cá thể - individuals).


Nhận xét:

Tính tối ưu: Không đảm bảo tìm ra trạng thái đích tối ưu (nếu có nhiều) và đường đi tìm được bởi A* sau đó cũng chỉ tối ưu cho trạng thái đích mà GA tìm được, không nhất thiết là đường đi tối ưu tổng thể từ trạng thái ban đầu.

Tính đầy đủ: Không đảm bảo. GA có thể hội tụ sớm về giải pháp dưới tối ưu hoặc không hội tụ nếu các tham số không phù hợp.

Độ phức tạp thời gian: Có thể rất chậm, phụ thuộc nhiều vào kích thước quần thể, số thế hệ, cách thực hiện các toán tử lai ghép/đột biến.

Độ phức tạp không gian (bộ nhớ): Cao.


![ScreenRecording2025-05-12022348-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d1649811-acea-47d4-b0f4-a554c216d252)




Thuật toán Local Beam Search

Ý tưởng:


Nhận xét:
Tính tối ưu: Không.

Tính đầy đủ: Không.

Độ phức tạp thời gian: Phụ thuộc vào k và số lượng trạng thái con sinh ra ở mỗi bước.

Độ phức tạp không gian (bộ nhớ): O(kb) hoặc O(k), tùy cách cài đặt. Bộ nhớ bị giới hạn bởi k, thường thấp hơn các thuật toán duyệt toàn bộ như A hay BFS. 


![ScreenRecording2025-05-12022917-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2202de07-38c9-40b6-8acd-7375f6a5dfd2)


4/CÁC THUẬT TOÁN CSPs

Thuật toán Backtracking:

Ý tưởng:

Là một cải tiến của DFS để giải các bài toán tìm kiếm, đặc biệt là CSP. Nó duyệt cây tìm kiếm theo chiều sâu. Tại mỗi nút, nó kiểm tra xem liệu có thể hoàn thành lời giải từ nút đó hay không. Nếu không (ví dụ, vi phạm ràng buộc trong CSP, hoặc đạt giới hạn độ sâu/gặp ngõ cụt trong tìm đường đi), nó sẽ quay lui (backtrack) lên nút cha và thử một nhánh khác. Trong ngữ cảnh tìm đường đi 8-puzzle, nó thực hiện một hành động, đi sâu, nếu không đạt đích hoặc gặp trạng thái đã thăm/giới hạn độ sâu thì quay lại và thử hành động khác

Nhận xét:

Tính tối ưu: Không. Không tìm được đường đi ngắn nhất.

Tính đầy đủ: Không.

Độ phức tạp thời gian: O(b^m). Có thể chậm.

Độ phức tạp không gian (bộ nhớ): O(b*m). Yêu cầu bộ nhớ thấp.



![ScreenRecording2025-05-12023846-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/e45a973e-8e3d-409b-8f7b-2c47f5ad5525)


Thuật toán Min-conflict:

Ý tưởng:

Min-Conflicts là chiến thuật “chọn ngẫu nhiên trong các hàng xóm tốt nhất”
giúp tránh kẹt đỉnh và duy trì sự đa dạng khi tối ưu cục bộ.
Rất thích hợp với bài toán hạn chế, cấu hình ràng buộc (constraint problems) như 8-puzzle, n-queens.

Nhận xét:
Tốc độ chạy: Rất nhanh vì không mở rộng toàn bộ cây
Khả năng tìm lời giải: không bảo đảm tìm thấy
Tối ưu lời giải: Không bảo đảm tìm đường đi ngắn nhất
Khả năng tránh đỉnh cục bộ: Trung bình, tốt hơn Hill-Climbing thường


![ScreenRecording2025-05-12024502-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/78dc3f78-6511-47e8-970b-595b3785786b)


