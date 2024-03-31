let socket = new WebSocket("ws://localhost:5001");

socket.onopen = function (e) {
  console.log("[open] Connection established");
  console.log("Sending to server");
  // socket.send("My name is John");
  socket.send("start_searching");
};

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log(data);
};
