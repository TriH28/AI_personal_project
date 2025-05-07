Báo cáo đồ án cá nhân (8-puzzles)

1.Mục tiêu

2.Nội dung

  2.1 Các thuật toán tìm kiếm không có thông tin (Uninformed Search)
  
   
    2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
    
        * Thuật toán BFS  (Breadth-First Search)
        
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
      2.1.2 Hình ảnh gif của các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin 
      
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
  
    2.1.1 Các thành phần chính của bài toán tìm kiếm và solution

    * Thuật toán A*

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
     2.1.2 Hình ảnh gif của các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin 
     ![Informed Search](https://github.com/user-attachments/assets/05bea791-c515-4709-ab8f-cd8aba78b2f7)




