// Hiện thông báo nếu có
  window.onload = function() {
    var notification = document.getElementById('notification');
    if (notification.classList.contains('show')) {
      setTimeout(function() {
        notification.classList.remove('show'); // Ẩn thông báo sau 3 giây
        notification.style.right = '-300px'; // Đưa ô thông báo ra ngoài
      }, 3000);
    }
  };