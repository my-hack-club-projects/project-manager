import axios from 'axios';

// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Create axios instance
const axiosInstance = axios.create({
  baseURL: '/',  // Adjust the base URL as per your API endpoint
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken'),
  },
});

function displayAlert(title, message) {
  if (window.vm && window.vm.config.globalProperties.$alert) {
    window.vm.config.globalProperties.$alert(title, message);
  } else {
    console.error('Vue instance is not available to display alert');
  }
}

// Add a response interceptor
axiosInstance.interceptors.response.use(
  response => {
    if (response.data && response.data.success !== true) {
      console.log('Response error:', response);
      const alertMessage = response.data.message || 'An unknown error occurred';
      const alertTitle = 'Error';

      displayAlert(alertTitle, alertMessage);

      return Promise.reject(alertMessage);
    }

    return response;
  },
  error => {
    // Handle errors globally if needed
    console.error('An error occurred:', error);

    displayAlert('Unknown client error', error);

    return Promise.reject(error);
  }
);

export default axiosInstance;
