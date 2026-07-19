document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('rpChatLauncher').addEventListener('click', function() {
    document.getElementById('rpChatPanel').classList.toggle('open');
  });
  document.getElementById('rpChatClose').addEventListener('click', function() {
    document.getElementById('rpChatPanel').classList.remove('open');
  });
});
