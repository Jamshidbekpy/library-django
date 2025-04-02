function addOrRemoveFavourite(resourceId) {
  console.log('Resource ID:', resourceId);

  let likeIcon = document.getElementById('like-icon-' + resourceId);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  

  const url = '/api/add-or-remove-favourite/'

  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        resource_id: resourceId,
      })
  })
      .then(response => response.json())
      .then(data => {
          if (data.isFavourite) {
              likeIcon.setAttribute('fill', '#f00');
              console.log('liked');
          } else {
              likeIcon.setAttribute('fill', '#fff');
              console.log('unliked');
          }
      })
      .catch((error) => {
          console.error('Error:', error);
      });


}