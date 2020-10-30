function loadVideo({ success, data }) {
      	if (!success) {
      		alert(`Error - ${data}`);
      		return;
      	}
      
      	// Hippity hoppity changing some proprieties ʕ•ᴥ•ʔ
      	document.querySelector('#video-title').innerText = data.title;
      	document.querySelector('#video-desc').innerHTML = data.description;
      	document.querySelector('#video-view').src = data.source;
      }
      
      const videoId = new URL(location).searchParams.get('id');
      
      if (videoId) {
      	// Basic jsonp implementation
      	const script = document.createElement('script');
      	script.src = `/videos/embed?id=${videoId}&callback=loadVideo`;
      	// Delete script from the DOM when failed / successed
      	['load', 'error'].forEach(e => {
      		script.addEventListener(e, () => script.remove());
      	});
      	// We are ready to go, load it !
      	document.body.appendChild(script);
      }
      
      // TODO: Add a way to call this function 
      // NOTE: Let the admin decide if this video is suitable for public listing
      // function requestListing() {
      // 	fetch(`/videos/listing-request`, {
      // 		method: 'POST',
      // 		headers: {
      // 			'Content-Type': 'application/x-www-form-urlencoded'
      // 		},
      // 		body: new URLSearchParams({
      // 			csrf: 'LiY4EMzluVaK+X5ukc4B2VOg5AqHZ9R4p4ghEQ25Kl4=',
      // 			url: window.location
      // 		})
      // 	});
      // }
      
      if (location.hash == '#debug') {
      	console.log('Current anti CSRF token is LiY4EMzluVaK+X5ukc4B2VOg5AqHZ9R4p4ghEQ25Kl4=');
      	// Easy way to display objects within a string
      	Object.prototype.toString = function () {
      		return JSON.stringify(this);
      	};
      }
