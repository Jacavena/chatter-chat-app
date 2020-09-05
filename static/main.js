(function() {
  function sendMessage() {
    console.log("WOW");
  };

  const logoutBtn = document.getElementsByClassName('logout-button')[0];
  const msgInput = document.getElementsByClassName('message-input')[0];
  const sendBtn = document.getElementsByClassName('send-button')[0];

  msgInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });

  sendBtn.onclick = sendMessage;
})();