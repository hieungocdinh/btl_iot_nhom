window.onload = function () {
  var notification = document.getElementById('notification');
  if (notification.classList.contains('show')) {
    setTimeout(function () {
      notification.classList.remove('show');
      notification.style.right = '-300px';
    }, 1500);
  }
};