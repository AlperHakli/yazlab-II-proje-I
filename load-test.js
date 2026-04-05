import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 50 },
    { duration: '20s', target: 100 },
    { duration: '20s', target: 200 },
    { duration: '20s', target: 500 },
    { duration: '20s', target: 0 },
  ],
};

export default function () {
  const res = http.get('http://host.docker.internal:8003/metrics');

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(1);
}

