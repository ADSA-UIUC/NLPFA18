// // Functions for drag and drop
// function allowDrop(ev) {
//   ev.preventDefault();
// }
//
// function drag(ev) {
//   ev.dataTransfer.setData("text", ev.target.id);
// }
//
// function drop(ev) {
//   ev.preventDefault();
//   var data = ev.dataTransfer.getData("text");
//   //ev.currentTarget.data-group = ev.target.data-group;
//   ev.target.appendChild(document.getElementById(data));
// }
//
// function dragenter(ev) {
//     // pass
// }
//
// function dragleave(ev) {
//     // pass
// }
//
//
// // Functions Grouping
// function updateGroup(ev) {
//     // change data for current group
//     // use https://www.quackit.com/html_5/tags/html_data_tag.cfm
// }
//
// function getGroups(ev) {
//     //var group1 = document.getElementById("group1")
//     //for each text ("text"+i) get group data
//     //  if data == none then dont analyze and show message "not all grouped"
// }


function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}
