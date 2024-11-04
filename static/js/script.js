function showNotifications() {
  const container = document.getElementById('notification-container');
  if (container.classList.contains('d-none')) {
    container.classList.remove('d-none');
  } else {
    container.classList.add('d-none');
  }
}


function getCookie(name) {
  let cookieValue = '';
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = docodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  };
  return cookieValue;
}

