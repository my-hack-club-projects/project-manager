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

function getErrorTitle(error) {
  if (error.response) {
    if (error.response.status === 401) {
      return "You don't have permission to view this resource!";
    } else if (error.response.status === 403) {
      return "You aren't allowed to do that!";
    } else if (error.response.status === 404) {
      return 'Not Found';
    }
  } else if (error.request) {
    return 'Network Error';
  } else {
    return 'Error';
  }
}

// Add a response interceptor
axiosInstance.interceptors.response.use(
  response => {
    if (response.data && response.data.success !== true) {
      const alertMessage = response.data.message || 'An unknown error occurred';
      const alertTitle = 'Error';

      displayAlert(alertTitle, alertMessage);

      return Promise.reject(alertMessage);
    }

    return response;
  },
  error => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
