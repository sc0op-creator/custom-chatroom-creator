const socket = io("ws://localhost:8080");

socket.on("message", (data) => {
  const el = document.createElement("li");
  el.innerHTML = data;
  document.querySelector("ul").appendChild(el);
});
document.getElementById("send").onclick = () => {
  let username = document.getElementById("username").value;
  let message = document.getElementById("message").value;
  socket.emit("message", `<${username}> ${message}`);
  document.getElementById("message").value = "";
};
// console.log("hello world")