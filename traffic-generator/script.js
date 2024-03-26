import http from 'k6/http';
import { sleep } from 'k6';

const simulate_traffic = () => {
  const stages = []
  const numStages = 20
  for (let i = 0; i < numStages; i++) {
    stages.push({ duration: '30s', target: 10 })
    stages.push({ duration: '2m', target: 50 })
    stages.push({ duration: '30s', target: 10 })
  }
  return stages
}

export let options = {
  stages: simulate_traffic()
};

export default function () {
  // Send a GET request to the specified URL
  const response = http.get('http://localhost:5000/');

  // Print the response status code to the console
  console.log('Response status code:', response.status);

  // Sleep for 1 second before sending the next request
  sleep(1);
}
