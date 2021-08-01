const socket = io("ws://localhost:8080");

socket.on("message", (data) => {
  const el = document.createElement("li");
  el.innerHTML = data;
  document.querySelector("ul").appendChild(el);
});
document.querySelector("#send").onclick = () => {
  let username = document.getElementById("username").value;
  let message = document.getElementById("message").value;
  let server_id = document.getElementById("server_id").value;
  let channel_id = document.getElementById("channel_id").value;
  socket.emit("message", `<${username}> ${message}`);
  fetch(`http://127.0.0.1:5000/server/${server_id}/channel/${channel_id}`, {
    method: "POST",
    body: JSON.stringify({'username' : username , 'message' : message}),
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  });
  document.getElementById("message").value = "";
};

// console.log("hello world")
