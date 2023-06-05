$(document).ready(function(){
  // Hide all sections except the first one on page load
  $('#orders-section').show();
  $('#positions-section').hide();

  // Show/hide sections based on clicked tab
  $('#orders-tab').click(function(){
      $('#orders-section').show();
      $('#positions-section').hide();
  });

  $('#positions-tab').click(function(){
      $('#orders-section').hide();
      $('#positions-section').show();
  });
})

const chartProperties = {
  width:1500,
  height:600,
  timeScale:{
    timeVisible:true,
    secondsVisible:false, 
  }
}