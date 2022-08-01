function getDataFromAPI() {
  const textarea = document.getElementById('textarea').value;
  textarea = textarea.replace(/\s+/g, '');
  const myArray = textarea.split(",");
  const json = JSON.stringify(myArray);
  console.log(json);
  
  fetch(`http://localhost:5000/winners_from_list?$values=${json}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById('result').innerHTML = data;
    });
}