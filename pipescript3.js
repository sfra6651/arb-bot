// Example steps in your JavaScript script
steps = 2;
for (let step = 1; step <= steps; step++) {
  // Simulate some work
  console.log((step / steps) * 100); // This will be written to stdout
  // Wait for a second to simulate a time-consuming task
  const start = new Date().getTime();
  while (new Date().getTime() - start < 1000);
}
