Báo cáo đồ án cá nhân (8-puzzles)

1.Mục tiêu

2.Nội dung

  2.1 Các thuật toán tìm kiếm không có thông tin (Uninformed Search)
  
   
    2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
   
        * Thuật toán BFS  (Breadth-First Search)
         ![BFS](https://github.com/user-attachments/assets/b2012eec-0dc5-4a25-bf56-e44b4e0a55c9)

          _ Các thành phần chính 
            + Hàng đợi (Queue)
              . Chức năng: Lưu trữ các trạng thái cần được xét theo thứ tự FIFO (First-In-First-Out)
              . Trong code: Sử dụng deque từ thư viện collections để tối ưu hiệu suất
            + Tập hợp đã thăm (Visited Set)
              . Chức năng: Theo dõi các trạng thái đã xét để tránh xét lại
            + Hàm tìm trạng thái lân cận
              . Chức năng: Tạo ra các trạng thái kế tiếp từ trạng thái hiện tại
            + Vòng lặp chính
              . Chức năng: Lấy trạng thái từ hàng đợi, kiểm tra mục tiêu, thêm trạng thái lân cận vào hàng đợi
          _ Solution từ BFS
            + Đặc điểm của solution
              . Tính đầy đủ: BFS luôn tìm được lời giải nếu tồn tại
              . Tối ưu: Tìm được lời giải ngắn nhất (ít bước nhất)
            + Cách biểu diễn solution trong code
              . Dạng đường đi: Một chuỗi các trạng thái từ start đến goal
            + Hiển thị solution
              . Trong giao diện: Hiển thị từng bước với độ trễ STEP_DELAY
            + Đánh giá hiệu suất
              . Thời gian thực thi: Được đo và hiển thị trên giao diện
        * Thuật toán DFS (Depth-First Search)
        ![DFS](https://github.com/user-attachments/assets/00621bd7-e316-4bed-8b48-da65dea5d590)

          _ Các thành phần chính 
            + Ngăn xếp (Stack)
              . Chức năng: Lưu trữ các trạng thái cần được xét theo thứ tự LIFO (Last-In-First-Out)
              . Trong code: Sử dụng list với cấu trúc (state, path, depth)
            + Tập hợp đã thăm (Visited Set)
              . Chức năng: Tương tự BFS, theo dõi các trạng thái đã xét
              . Khác biệt: Trong DFS thông thường không cần visited set nếu không có cycle, nhưng ở đây vẫn giữ để tối ưu
            + Giới hạn độ sâu (Depth Limit)
              . Chức năng: Ngăn DFS đi quá sâu vào một nhánh vô ích
            + Hàm tìm trạng thái lân cận
              . Giống BFS: Sử dụng cùng hàm get_neighbors() hoặc logic tương tự
          _ Solution từ DFS
            + Đặc điểm Solution DFS
              . Không đảm bảo tối ưu: Solution có thể dài hơn nhiều so với solution ngắn nhất mà BFS tìm được
              . Phụ thuộc vào thứ tự duyệt: Thay đổi thứ tự duyệt các hướng (UP, DOWN, LEFT, RIGHT) sẽ cho solution khác nhau
              . Có thể không tìm thấy solution nếu đặt depth_limit quá nhỏ
            + Cách biểu diễn solution trong code
              . Cách lưu trữ dùng stack = [(start_state, [start_state], 0)]  
        * Thuật toán UCS (Uniform Cost Search)
        ![UCS](https://github.com/user-attachments/assets/d5990234-7189-4aae-b3c3-696ac2e479d4)

          _ Các thành phần chính 
            + Hàng đợi ưu tiên (Priority Queue)
              . Chức năng: Lưu trữ các trạng thái cần xét theo chi phí tăng dần
              . Triển khai: Sử dụng heapq để tối ưu hiệu suất
            + Tập hợp đã thăm (Visited Set)
              . Chức năng: Tránh xét lại các trạng thái đã duyệt
            + Hàm tính chi phí
              . Đặc điểm: Trong UCS cho 8-puzzle, mỗi bước di chuyển có chi phí bằng nhau (1)
          _ Solution từ UCS
            + Tối ưu
              . UCS luôn tìm ra lộ trình có tổng chi phí thấp nhất, tức là ít bước nhất nếu mỗi bước có cùng chi phí
            + Chính xác
              . Luôn đảm bảo đến được goal_state, nếu có tồn tại đường đi.
            + Cách UCS sinh ra solution
              . UCS sử dụng một priority queue (hàng đợi ưu tiên) để mở rộng trạng thái có chi phí thấp nhất trước
              . Với mỗi trạng thái mới sinh ra, thuật toán lưu lại trạng thái cha để có thể truy vết lại đường đi sau khi tìm thấy goal_state
              . Khi đạt đến trạng thái đích, thuật toán lần ngược từ goal về start để tái tạo lại chuỗi bước đi hoàn chỉnh — đó chính là solution
        * Thuật toán IDDFS (Iterative Deepening Depth-First Search)
        ![IDDFS](https://github.com/user-attachments/assets/d221a78a-f1c7-44c0-a056-1d91e14961b0)

          _ Các thành phần chính 
            + Hàm chính: iddfs(start, goal)
              . Là vòng lặp vô hạn (while True) để thử từng giới hạn độ sâu depth_limit
              . Tại mỗi bước lặp, gọi hàm dfs(start, goal, depth_limit) để tìm kiếm trạng thái đích trong phạm vi độ sâu hiện tại
            +  Chiến lược tìm kiếm
              . Bắt đầu với độ sâu = 0 (chỉ kiểm tra start)
              . Sau đó thử với độ sâu = 1, 2, 3... tăng dần
              . Mỗi lần đều dùng DFS giới hạn độ sâu để đảm bảo không đi quá xa hoặc vào vòng lặp vô hạn
            + Hàm phụ dfs(state, goal, depth_limit)
              . Duyệt các trạng thái theo kiểu hậu duệ trước (depth-first) nhưng không vượt quá độ sâu cho phép
              . Trả về đường đi (solution) nếu tìm thấy trạng thái đích trong phạm vi độ sâu đó
              . Nếu không tìm thấy gì trong độ sâu đó → quay lại iddfs để tăng giới hạn và thử lại
          _ Solution từ UCS
            + Tìm kiếm toàn diện
              . IDDFS không bỏ sót trạng thái nào, nếu trạng thái đích tồn tại, chắc chắn sẽ tìm thấy
            + Bảo đảm tìm được đường đi ngắn nhất theo độ sâu
              . Vì tìm từ độ sâu 0 → ∞ nên sẽ bắt gặp trạng thái đích sớm nhất có thể
            + Tái sử dụng bộ nhớ hiệu quả
              . Mỗi lần gọi DFS đều dùng ít bộ nhớ (chỉ lưu ngăn xếp), không lưu toàn bộ cây trạng thái như BFS
            + Lặp lại tính toán
              . Có thể duyệt lại cùng một nút nhiều lần trong các độ sâu khác nhau (trade-off giữa thời gian và bộ nhớ)
      2.1.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin 
      
      ![Uninformed Search](https://github.com/user-attachments/assets/f2f01427-114f-4133-915f-2de905267f40)
      
      2.1.3 Nhận xét về hiệu suất các thuật toán
        _ BFS
          + BFS là thuật toán duyệt theo từng lớp (tầng), tức là xét hết các trạng thái có cùng độ sâu trước khi tiến sâu hơn. Trong giải bài toán 8-puzzle, BFS bắt đầu từ trạng thái gốc, sau đó lần lượt mở rộng tất cả các trạng thái con từ vị trí ô trống (blank tile), kiểm tra từng trạng thái mới tạo ra để xem có đạt trạng thái đích hay chưa
          + Ưu điểm chính của BFS là bảo đảm tìm được lời giải ngắn nhất (ít bước nhất), vì nó luôn duyệt theo mức độ sâu tăng dần. Tuy nhiên, nhược điểm lớn nhất là chiếm nhiều bộ nhớ, vì phải lưu toàn bộ các trạng thái ở mỗi mức độ sâu. Với các bài toán có không gian trạng thái lớn như 8-puzzle, BFS có thể nhanh chóng tiêu tốn tài nguyên nếu độ sâu của lời giải tăng cao
        _ DFS
          + DFS hoạt động theo chiến lược “đi sâu đến tận cùng trước rồi mới quay lại”, rất tiết kiệm bộ nhớ vì không cần lưu toàn bộ không gian trạng thái đang xét. Tuy nhiên, DFS truyền thống có thể bị lặp vô hạn hoặc đi sâu mà không bao giờ quay lại. Do đó, biến thể DFS có giới hạn độ sâu (depth-limited) được sử dụng: thuật toán chỉ tìm kiếm đến một độ sâu nhất định rồi dừng lại
          + Tuy giải pháp này giảm đáng kể chi phí bộ nhớ, nhưng có nguy cơ bỏ sót lời giải nếu giới hạn quá thấp, và không đảm bảo tìm được lời giải ngắn nhất
        _ IDDFS
          + IDDFS là sự kết hợp của BFS và DFS: nó dùng DFS nhưng lặp lại nhiều lần với độ sâu tăng dần từ 0, 1, 2, ..., cho đến khi tìm được lời giải. Điều này giúp khắc phục cả hai nhược điểm:
            . Không tốn nhiều bộ nhớ như BFS
            . Đảm bảo tìm được lời giải ngắn nhất như BFS, vì mỗi lần đều kiểm tra toàn bộ các đường đi ngắn hơn trước khi tăng độ sâu
        _ UCS
          + UCS là thuật toán sử dụng hàng đợi ưu tiên để luôn mở rộng trạng thái có tổng chi phí thấp nhất tính từ gốc đến hiện tại. Trong 8-puzzle, nếu mỗi bước di chuyển đều có chi phí như nhau (ví dụ mỗi bước đều là 1), thì UCS hoạt động tương tự như BFS
          + Tuy nhiên, UCS thực sự mạnh khi các bước có chi phí khác nhau, như trong các bài toán có trọng số đường đi khác nhau. Khi đó, UCS đảm bảo tìm ra lời giải tối ưu về chi phí, chứ không chỉ ngắn về số bước. UCS vẫn cần bộ nhớ lớn như BFS để lưu và sắp xếp các trạng thái trong hàng đợi ưu tiên

  2.2 Các thuật toán tìm kiếm có thông tin (Informed Search)
  
    2.2.1 Các thành phần chính của bài toán tìm kiếm và solution

    * Thuật toán A*
    ![A*](https://github.com/user-attachments/assets/4cdfb8e3-f0a8-42cd-a333-5deec17266cc)


      _ Các thành phần chính
        + Hàm heuristic (Manhattan Distance)
          . Tính tổng khoảng cách từ vị trí hiện tại của mỗi ô đến vị trí đích của nó
          . Đảm bảo heuristic là admissible (không đánh giá quá chi phí thực tế)
        + Hàng đợi ưu tiên (Priority Queue)
          . Sắp xếp các trạng thái cần xét theo tổng chi phí (f(n) = g(n) + h(n))
          . Sử dụng module heapq để triển khai min-heap
        + Tập hợp các trạng thái đã xét (Visited Set)
          . Tránh xét lại các trạng thái đã xét trước đó
          . Tối ưu hiệu suất thuật toán
        + Hàm tìm kiếm lân cận (Neighbor Function)
          . Tạo ra các trạng thái kế tiếp bằng cách di chuyển ô trống
      _ Solution từ A*
        + Đặc điểm 
          . Là solution tối ưu (ít bước nhất) vì heuristic Manhattan distance là admissible
          . Số bước trong solution phụ thuộc vào độ phức tạp của trạng thái ban đầu
          . Thời gian tìm solution thường nhanh hơn BFS/DFS do sử dụng heuristic
        + Hiển thị trong chương trình
          . Solution được hiển thị từng bước với delay STEP_DELAY = 300ms
          . Thông tin thời gian thực thi được hiển thị: "Execution Time: x.xxxx seconds"
          . Các ô được highlight khi di chuyển
          
    * Thuật toán IDA*
    ![IDA*](https://github.com/user-attachments/assets/70113acf-75cc-44ab-9466-45be8b16b6fe)

      _ Các thành phần chính
        + Hàm heuristic (Manhattan Distance)
          . Sử dụng khoảng cách Manhattan làm heuristic
          . Đảm bảo tính admissible (không đánh giá quá chi phí thực tế)
        + Hàm tìm kiếm chính (ida_star_search)
          . Khởi tạo giới hạn (bound) ban đầu bằng heuristic của trạng thái bắt đầu
          . Duy trì đường đi hiện tại trong biến path
        + Hàm tìm kiếm đệ quy (search)
          . g: chi phí từ trạng thái ban đầu đến trạng thái hiện tại
          . Tính f = g + h(state) (chi phí + heuristic)
          . Nếu vượt quá giới hạn, trả về giá trị f mới
          . Nếu tìm thấy goal, trả về "FOUND"
        + Phần mở rộng trạng thái
          . Duyệt qua các hướng di chuyển có thể của ô trống
          . Tạo trạng thái mới và kiểm tra chưa tồn tại trong path
          . Gọi đệ quy hàm search với chi phí tăng lên 1
          . Cập nhật giới hạn nhỏ nhất nếu tìm thấy giá trị tốt hơn
        + Vòng lặp chính
          . Lặp lại quá trình tìm kiếm với bound mới
          . Dừng khi tìm thấy solution hoặc không tìm thấy (float('inf'))
      _ Solution từ IDA*
        + Đặc điểm 
          . Tối ưu: Giống A*, tìm đường đi ngắn nhất do sử dụng heuristic admissible
          . Tiết kiệm bộ nhớ: Chỉ lưu đường đi hiện tại thay vì toàn bộ không gian trạng thái
          . Từng bước lặp: Mỗi lần lặp tăng dần giới hạn bound cho đến khi tìm thấy solution
        + Hiển thị trong chương trình
          . Solution được hiển thị từng bước với delay STEP_DELAY
          . Thông tin thời gian thực thi được hiển thị
          . Các ô được highlight khi di chuyển

    * Thuật toán Greedy Search
    ![Greedy](https://github.com/user-attachments/assets/f23de7ea-24c6-465a-b365-e88b7faa0fae)

      _ Các thành phần chính
        + Hàm heuristic (Manhattan Distance)
          . Ước lượng chi phí từ trạng thái hiện tại đến trạng thái đích
          . Sử dụng khoảng cách Manhattan (tổng khoảng cách dọc và ngang)
        + Hàng đợi ưu tiên (Priority Queue)
          . Sắp xếp các trạng thái dựa trên giá trị heuristic
          . Sử dụng module heapq để triển khai min-heap
        + Tập hợp các trạng thái đã xét (Visited Set)
          . Theo dõi các trạng thái đã được xử lý
          . Tránh xét lại các trạng thái trùng lặp
      _ Solution từ Greedy Search

        + Đặc điểm 
          . Không đảm bảo tối ưu: Có thể không tìm được đường đi ngắn nhất
          . Không đảm bảo đầy đủ: Có thể bị kẹt trong vòng lặp vô hạn nếu không có cơ chế kiểm soát
          . Nhanh chóng: Thường tìm được solution nhanh do tập trung vào heuristic
        + Ưu điểm
          . Triển khai đơn giản
          . Tốc độ nhanh trong nhiều trường hợp
          . Hiệu quả với heuristic tốt
        + Nhược điểm
          . Dễ bị mắc kẹt ở local optimum
          . Không đảm bảo tìm được solution
          . Chất lượng solution phụ thuộc nhiều vào heuristic
     2.2.2 Hình ảnh gif của các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin 
     ![Informed Search](https://github.com/user-attachments/assets/05bea791-c515-4709-ab8f-cd8aba78b2f7)
     2.2.3 Nhận xét về hiệu suất các thuật toán
       _ A* (A-star)
         + Ưu điểm
           . Tối ưu (luôn tìm được lời giải ngắn nhất nếu tồn tại)
           . Hiệu quả với heuristic Manhattan Distance
           . Thời gian chạy tốt trong hầu hết trường hợp
          + Nhược điểm
            . Tiêu tốn bộ nhớ do lưu trữ nhiều trạng thái
            . Phức tạp khi kích thước puzzle tăng
        _ UCS (Uniform Cost Search)
          + Ưu điểm
            . Tối ưu như A*
            . Đơn giản hơn A*
          + Nhược điểm
            . Chậm hơn A* do không sử dụng heuristic
            . Duyệt nhiều node không cần thiết
        _ Greedy
          + Ưu điểm
            . Nhanh trong nhiều trường hợp
            . Tập trung vào mục tiêu
          + Nhược điểm
            . Không đảm bảo tối ưu
            . Dễ bị kẹt trong local optima

2.3 Các thuật toán tìm kiếm nội bộ

    2.3.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán simple hill climbing
        ![Simple Hill Climbing](https://github.com/user-attachments/assets/d36e9cce-164c-454a-b450-7de1f3c1790f)

          _ Các thành phần chính
            + Hàm đánh giá (Heuristic Function)
              . Sử dụng khoảng cách Manhattan để đánh giá trạng thái hiện tại
              . manhattan_distance(state) tính tổng khoảng cách từ vị trí hiện tại của các ô đến vị trí đích
            + Trạng thái hiện tại (Current State)
              . Bắt đầu từ trạng thái ban đầu (start_state)
              . Theo dõi trạng thái hiện tại trong quá trình tìm kiếm
            + Hàng xóm (Neighbors)
              . get_neighbors(state) tạo ra các trạng thái kế tiếp bằng cách di chuyển ô trống
              . Mỗi trạng thái có tối đa 4 hàng xóm (lên, xuống, trái, phải)
            + Lựa chọn bước đi
              . So sánh giá trị heuristic của các hàng xóm
              . Chọn hàng xóm có giá trị heuristic tốt nhất (nhỏ nhất)
            + Xử lý local optimum:
              . Bộ đếm stuck_count để phát hiện khi bị kẹt
              . Khi bị kẹt (>5 lần), thực hiện bước đi ngẫu nhiên có kiểm soát
              . Cho phép di chuyển ngang (cùng giá trị heuristic) để thoát local optimum
          _ Solution từ Simple hill climbing
            + Ưu điểm
              . Thuật toán chỉ cần so sánh các trạng thái lân cận
              . Không cần lưu trữ nhiều trạng thái như BFS/DFS
              . Chỉ lưu trữ đường đi hiện tại
              . Không cần hàng đợi hoặc ngăn xếp như các thuật toán khác
              . Với 8-puzzle 3x3, thường tìm được giải pháp khá nhanh
            + Nhược điểm
              . Khi gặp trạng thái mà mọi hàng xóm đều xấu hơn
              . Có thể không tìm thấy giải pháp tối ưu
              . Phụ thuộc vào trạng thái ban đầu
              . Thời gian chạy thay đổi tùy vào trạng thái ban đầu
              . Có thể cần nhiều lần thử để tìm ra giải pháp

      * Thuật toán Steepest ascent hill climbing
        ![Steepest Ascen Hill Climbing](https://github.com/user-attachments/assets/dce830da-ab74-4398-8499-be9c442ec1d5) 
        _ Các thành phần chính
          + Hàm Heuristic (Manhattan Distance)
            . Đánh giá "độ tốt" của một trạng thái
            . Tính tổng khoảng cách từ vị trí hiện tại của các ô đến vị trí đích của chúng
          + Trạng thái hiện tại (Current State)
            . Khởi tạo: Bắt đầu từ start_state
            . Cập nhật: Liên tục thay đổi khi tìm được trạng thái tốt hơn
          + Hàng xóm (Neighbors)
            . Di chuyển ô trống (0) lên/xuống/trái/phải (nếu hợp lệ)
            . Mỗi trạng thái có tối đa 4 hàng xóm
          + Lựa chọn bước đi (Steepest Ascent)
            . Không chọn hàng xóm đầu tiên tốt hơn.
            . Duyệt tất cả hàng xóm và chọn trạng thái tốt nhất (có manhattan_distance nhỏ nhất)
          + Xử lý Local Optimum (Tối ưu cục bộ)
            . Chọn ngẫu nhiên một hàng xóm để thoát khỏi bế tắc
          + Giới hạn số lần thử (max_attempts)
            . Nếu vượt quá max_attempts mà chưa tìm ra giải pháp → Dừng thuật toán
        _ Solution từ Steepest ascent hill climbing
          + Ưu điểm
            . Luôn chọn bước đi tối ưu nhất trong các hàng xóm → Giảm số bước không cần thiết
            . Nếu không tìm được trạng thái tốt hơn → Di chuyển ngẫu nhiên để tránh bị kẹt
            . Chỉ lưu đường đi hiện tại, không cần hàng đợi/ngăn xếp như BFS/DFS
          + Nhược điểm
            . Nếu không có hàng xóm nào tốt hơn, thuật toán phải chọn ngẫu nhiên → Không đảm bảo tìm ra giải pháp
            . Có thể tìm được giải pháp không phải ngắn nhất
            . Nếu start_state xa goal_state, thuật toán có thể chạy lâu hơn

      * Thuật toán Stochastic hill climbing
      ![Stochastic Hill](https://github.com/user-attachments/assets/5f3e58d1-c941-43d7-a10f-14e0cb6fd485)

        _ Các thành phần chính
          + Hàm Heuristic (Manhattan Distance)
            . Sử dụng manhattan_distance(state) để đánh giá chất lượng trạng thái
            . Khoảng cách càng nhỏ → trạng thái càng tốt
          + Lựa chọn hàng xóm theo xác suất
            . Không chọn hàng xóm tốt nhất
            . Gán xác suất chọn cho từng hàng xóm tốt hơn hoặc bằng
          +  Cơ chế tính xác suất
          + Chọn lựa ngẫu nhiên có trọng số
          + Xử lý local optimum
        _ Solution từ Stochastic hill climbing
          + Ưu điểm
            . Nhờ cơ chế chọn ngẫu nhiên có trọng số
            . Vẫn ưu tiên các trạng thái tốt nhưng không cứng nhắc
            . Có thể thử nghiệm nhiều hướng đi khác nhau
            . Giảm khả năng bị kẹt vào cùng một đường đi
            . Trạng thái chỉ tốt hơn một chút vẫn có cơ hội được chọn
          + Nhược điểm
            . Có thể mất nhiều bước hơn do chọn ngẫu nhiên
            . Không chắc chắn tìm được giải pháp tối ưu
            . Cách tính xác suất ảnh hưởng lớn đến hiệu quả
            . Cần điều chỉnh hệ số (+0.1) cho phù hợp
            . Các lần chạy khác nhau có thể cho kết quả khác nhau
      * Thuật toán Simulated annealing
      ![Simulated Annealing](https://github.com/user-attachments/assets/86f53cf9-7952-4254-95ff-7f03526faf84)

        _ Các thành phần chính 
          + Hàm đánh giá (Energy Function)
            . Sử dụng manhattan_distance(state) làm hàm năng lượng
            . Mục tiêu: Giảm thiểu giá trị này (tương tự như trong vật lý, hệ thống tiến tới trạng thái năng lượng thấp nhất)
          + Tham số nhiệt độ
            . Nhiệt độ ban đầu (initial_temp) thường chọn giá trị lớn (1000 trong code) để cho phép khám phá mạnh ban đầu
            . Tỉ lệ làm mát (cooling_rate), giá trị 0.99 giảm nhiệt độ từ từ, temp *= cooling_rate sau mỗi lần lặp
          + Cơ chế chấp nhận bước đi
          + Tiêu chí dừng
            . Tìm thấy trạng thái đích
            . Đạt số lần lặp tối đa (max_iterations)
            . Nhiệt độ giảm xuống quá thấp (temp < 0.1)
        _ Solution từ Simulated annealing
          + Ưu điểm 
            . Khả năng thoát local optimum mạnh mẽ
            . Cân bằng giữa exploration và exploitation
            . Không phụ thuộc vào trạng thái ban đầu
          + Nhược điểm
            . Phụ thuộc vào tham số initial_temp quá thấp → thiếu khám phá, cooling_rate quá nhanh → hội tụ sớm
            . Tốc độ chậm do phải tính toán xác suất và quản lý nhiệt độ
            . Không đảm bảo tìm được giải pháp tối ưu
      * Thuật toán Beam Search
      ![Beam](https://github.com/user-attachments/assets/a2a6e367-44d1-40ed-aa60-01699f8fc212)

        _ Các thành phần chính
          + Hàm đánh giá (Evaluation Function)
            . Sử dụng manhattan_distance(state) để đánh giá chất lượng trạng thái
            . Mục tiêu là tìm trạng thái có giá trị heuristic nhỏ nhất
          + Beam Width (Bề rộng chùm)
            . Tham số beam_width (mặc định là 2) quyết định: số lượng trạng thái tốt nhất được giữ lại sau mỗi bước và cân bằng giữa hiệu suất và chất lượng giải pháp
          + Cơ chế tìm kiếm theo tần
          + Quản lý các trạng thái đã thăm
            . Sử dụng tập hợp visited để tránh lặp lại trạng thái
        _ Solution từ Beam Search
          + Ưu điểm
            . Cân bằng giữa BFS và Greedy Search
            . Không chỉ chọn 1 trạng thái tốt nhất như Greedy (giảm rủi ro bỏ sót giải pháp
            . Kiểm soát được không gian tìm kiếm
            . Tránh lặp trạng thái
          + Nhược điểm
            . Không đảm bảo tìm ra giải pháp
            . Phụ thuộc vào hàm heurist
            . Không có cơ chế thoát local optimum
      * Thuật toán Genetic
      ![Genetic](https://github.com/user-attachments/assets/66a437e8-8c68-4b06-bc3c-d75c232f565a)

        _ Các thành phần chính
          + Biểu diễn cá thể (Individual Representation)
            . Mỗi cá thể là một chuỗi các trạng thái (path) từ start state
          + Hàm đánh giá (Fitness Function)
            . Sử dụng khoảng cách Manhattan làm độ đo
            . Giá trị càng thấp → cá thể càng tốt
          + Khởi tạo quần thể (Initial Population)
            . Mỗi cá thể được tạo bằng cách thực hiện các bước di chuyển ngẫu nhiên từ start state
          + Chọn lọc (Selection)
            . Chọn ngẫu nhiên 3 cá thể → giữ lại cá thể tốt nhất
          + Lai ghép (Crossover)
            . Ghép 2 path từ 2 cha mẹ tại điểm ngẫu nhiên
          + Đột biến (Mutation)
            . Thay đổi ngẫu nhiên một trạng thái trong path
            . Đảm bảo tính hợp lệ của path sau đột biến
          + Tham số thuật toán
            . population_size: Số lượng cá thể (50)
            . generations: Số thế hệ (1000)
            . mutation_rate: Xác suất đột biến (0.2)
        _ Phân tích solution
          + Ưu điểm
            . Không cần heuristic phức tạp
            . Khám phá không gian giải pháp đa dạng nhờ cơ chế đột biến và lai ghép, tránh được local optimum tốt hơn các phương pháp leo đồi
            . Linh hoạt trong biểu diễn bài toán có thể dễ dàng áp dụng cho các phiên bản puzzle khác nhau
          +Nhược điểm
            . Tốn chi phí tính toán
            . Cần duy trì và đánh giá cả quần thể
            . Không đảm bảo tìm ra giải pháp tối ưu
            . Phụ thuộc vào may mắn trong quá trình tiến hóa
            . Có thể hội tụ sớm vào giải pháp dưới tối ưu
            .  Điều chỉnh tham số phức tạp
            . Cần tinh chỉnh population_size, mutation_rate cho từng bài toán
    2.3.2 Hình ảnh gif của các thuật toán trong nhóm thuật toán tìm kiếm nội bộ
    ![Local Search](https://github.com/user-attachments/assets/1ee15406-a9bb-42fd-ba0e-b54908494bdd)


2.4 Các thuật toán tìm kiếm trong môi trường phức tạp

     2.3.1 Các thành phần chính của bài toán tìm kiếm và solution
       * Thuật toán Nondeterministic Search
       ![Nondeterministic Search](https://github.com/user-attachments/assets/a53fb3f8-154b-434b-ba95-8a5f258f651e)
       
         _ Các thành phần chính
           + Hàm heuristic kỳ vọng (expected_heuristic)
             . Mục đích: Điều chỉnh heuristic thông thường để tính đến yếu tố không xác định
             . Cách tính: Nhân khoảng cách Manhattan với hệ số 1/xác_suất_thành_công
             . Ý nghĩa: Khi xác suất thành công thấp, heuristic giá trị cao hơn để phản ánh độ khó
            + Cấu trúc dữ liệu và khởi tạo
              . Open set: Hàng đợi ưu tiên lưu (f_score, cost, state, path)
              . Visited set: Tập hợp các trạng thái đã xét để tránh lặp
            + Vòng lặp chính
              . Lấy trạng thái có f_score nhỏ nhất từ open set
              . Kiểm tra điều kiện dừng khi gặp goal state
              . Bỏ qua các trạng thái đã xét
            + Xử lý hành động không xác định
              . Tìm các trạng thái kề có thể có
              . Trong phiên bản đơn giản này, chỉ xét trạng thái mong muốn (không xét các trạng thái lỗi)
          _ Phân tích solution
            + Ưu điểm
              . Kế thừa ưu điểm của A*: Đảm bảo tìm được lời giải tối ưu nếu tồn tại
              . Xử lý không xác định: Heuristic điều chỉnh phản ánh độ không chắc chắn
              . Hiệu quả: Vẫn duy trì được tính hiệu quả của A* trong môi trường không xác định
            + Nhược điểm
              . Phiên bản đơn giản hóa: Chỉ xét trạng thái mong muốn, không mô hình hóa đầy đủ các kết quả có thể có
              . Heuristic đơn giản: Chỉ nhân hệ số cố định, chưa phản ánh chính xác xác suất các trạng thái khác nhau
        * Thuật toán Partial Observation
        ![Partial Observation](https://github.com/user-attachments/assets/17d178e2-ae45-4161-82c8-ceacf257322d)

          _ Các thành phần chính
            + Khởi tạo quan sát một phần
              . Mục đích: Tạo trạng thái quan sát ban đầu với một số ô bị ẩn
              . Cách hoạt động: Chọn ngẫu nhiên num_hidden ô để ẩn, chỉ giữ lại giá trị các ô hiển thị
            + Belief States (Trạng thái niềm tin)
              . Định nghĩa: Tập hợp tất cả các trạng thái có thể phù hợp với quan sát hiện tại
              . Trong triển khai đơn giản: Chỉ sử dụng trạng thái thực (để minh họa)
              . Triển khai đầy đủ: Cần sinh tất cả trạng thái có thể khớp với các ô đã quan sát
            + Vòng lặp tìm kiếm chính
              . Vòng lặp tìm kiếm chính
              . Mỗi bước: Chọn hành động, thực hiện di chuyển, cập nhật thông tin
            + Cập nhật quan sát
              . Quy tắc: Ô trống (0) luôn được tiết lộ khi nó di chuyển vào vị trí bị ẩn
              . Mục đích: Giảm dần số ô bị ẩn khi puzzle được giải
            + Cập nhật Belief States
              . Chức năng: Lọc các trạng thái trong belief states để chỉ giữ lại những cái phù hợp với quan sát mới
              . Triển khai đầy đủ: Cần kiểm tra tính nhất quán của mỗi trạng thái với observation
          _ Phân tích solution
            + Ưu điểm
              . Mô phỏng quan sát không đầy đủ: Giải quyết bài toán thực tế khi không thấy toàn bộ trạng thái
              . Tiếp cận Belief State: Phù hợp với lý thuyết POMDP (Partially Observable MDP)
              . Cơ chế tiết lộ thông tin: Tự động phát hiện ô trống khi nó di chuyển vào vị trí ẩn
            + Nhược điểm
              . Triển khai đơn giản hóa: Chưa thực sự quản lý belief states đầy đủ
              . Chiến lược chọn hành động ngẫu nhiên: Không tối ưu, có thể dẫn đến hiệu suất thấp
              . Thiếu cơ chế xử lý khi belief states rỗng: Không xử lý trường hợp không có trạng thái nào phù hợp
              
            Giải pháp Partial Observation Search cung cấp cách tiếp cận hợp lý cho bài toán 8-puzzle với thông tin không đầy đủ. Phiên bản hiện tại là một khung cơ bản tốt
            
    2.3.2 Hình ảnh gif của các thuật toán trong nhóm thuật toán tìm kiếm nội bộ
    ![Complex Environment](https://github.com/user-attachments/assets/2ff080f6-a24d-477a-9ead-9de03e443df9)



    








        


        





