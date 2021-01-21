// código jQuery que se ejecuta al cargar la página
$(function () {
  // Dark Mode
  $('#modo').click(function(){
    var element = document.body;
    element.classList.toggle("dark-mode");
  });

  $( document ).ready(function(){
    var $fila = $('#fila')

    $.ajax({
      type:'GET',
      url: 'http://0.0.0.0:5000/api/friends',
      success:function(episodes){
        $.each(episodes, function(i, episode){
          $fila.append('<tr><td>' + episode.name + '</td><td>' + episode.season + '</td><td>' + episode.number + '</td><td>' + episode.airdate + '</td><td>' + episode.summary + `</td><td> <input onclick="Borrar('${episode.id}')" type="image" alt="delete" src="static/images/delete.png" height="25" width="25"/> </td></tr>`)
        });
      }
    });
  });

  // evento para cuando cambia el valor introducido en un <input id="buscar" $gt;
  $('#buscar').keyup(function(){
    let value = $(this).val()
    var request_url = 'http://0.0.0.0:5000/api/friends/' + value
    var $fila = $('#fila')

    if(value == ""){
      request_url = 'http://0.0.0.0:5000/api/friends'
    }

    $.ajax({
      type:'GET',
      url: request_url,
      success:function(episodes){
        // Limpiar consulta anterior
        var div = document.getElementById('fila');
        while (div.firstChild) {
            div.removeChild(div.firstChild);
        }

        $.each(episodes, function(i, episode){
          $fila.append('<tr><td>' + episode.name + '</td><td>' + episode.season + '</td><td>' + episode.number + '</td><td>' + episode.airdate + '</td><td>' + episode.summary + `</td><td> <input onclick="Borrar('${episode.id}')" type="image" alt="delete" src="static/images/delete.png" height="25" width="25"/> </td></tr>`)
        });
      }
    });
  });
});

// Click en el botón
function Borrar(id) {
  // Para poner otra vez funciones jQuery en el DOM actual
  $(function () {
    var request_url = 'http://0.0.0.0:5000/api/friends/' + id
    $.ajax({
      url: request_url,
      type:'DELETE',
      success:function(result){
        
      }
    });

    var value = $('#buscar').val()
    request_url = 'http://0.0.0.0:5000/api/friends/' + value
    var $fila = $('#fila')
    
    if(value == ""){
      request_url = 'http://0.0.0.0:5000/api/friends'
    }
    
    // Limpiar consulta anterior
    var div = document.getElementById('fila');
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }

    $.ajax({
      type:'GET',
      url: request_url,
      success:function(episodes){
        
        $.each(episodes, function(i, episode){
          $fila.append('<tr><td>' + episode.name + '</td><td>' + episode.season + '</td><td>' + episode.number + '</td><td>' + episode.airdate + '</td><td>' + episode.summary + `</td><td> <input onclick="Borrar('${episode.id}')" type="image" alt="delete" src="static/images/delete.png" height="25" width="25"/> </td></tr>`)
        });
      }
    });
  });
}