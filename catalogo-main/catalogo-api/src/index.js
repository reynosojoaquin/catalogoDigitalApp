import app from './app';
import '@babel/polyfill';
 import testData from './database/testData';

async function main() {
  await app.listen(process.env.PORT);
  
  if (process.env.FORCE_SYNC === 'true') {
           testData();
  }
  console.log(`Server running: http://localhost:${process.env.PORT} ✅`);
}
 

main();
