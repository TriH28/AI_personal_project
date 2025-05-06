Báo cáo đồ án cá nhân (8-puzzles)
1.Mục tiêu
2.Nội dung
  2.1 Các thuật toán tìm kiếm không có thông tin 
    2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
        * Thuật toán BFS  (Breadth-First Search)
          _ Các thành phần chính của BFS
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
          _ Các thành phần chính của DFS 
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
          _ Các thành phần chính của UCS
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
          _ Các thành phần chính của IDDFS
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
      
      


              
              
              

              
      
              






          


