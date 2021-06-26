const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('reddit' , (result) => {
  });
});

sio.on('disconnect', () => {
    console.log("disconnected");
});

sio.on("comment", (data) => {
    // console.log(data)
    var tbodyRef = document.getElementById('statsTable').getElementsByTagName('tbody')[0];
    var row = tbodyRef.insertRow();

    cell_flair = row.insertCell(0)
    cell_sa1 = row.insertCell(1)
    cell_sa2 = row.insertCell(2)
    cell_comment = row.insertCell(3)

    // using innerText is safer, but presumably the Reddit API has already scrubbed the comments
    cell_flair.innerHTML = data["flair"]
    cell_sa1.innerHTML = data["sa1"]
    cell_sa2.innerHTML = data["sa2"]
    cell_comment.innerHTML = data["comment"]

    // if desired, auto-scroll to the display's bottom
    // window.scrollTo(0,document.body.scrollHeight);

});
