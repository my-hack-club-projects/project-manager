import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: '/api/',  // Adjust the base URL as per your API endpoint
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken'),  // Function to get CSRF token from cookies
  },
});

// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

export default axiosInstance;