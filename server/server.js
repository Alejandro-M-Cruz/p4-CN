import express from 'express'

const app = express()

app.get('/', (req, res) => {
  res.send('<h1>Hello, world!</h1>')
})

app.get('/about', (req, res) => {
  res.send('<h1>About page</h1>')
})

app.listen(80, () => {
  console.log('Server is listening on port 80')
})
