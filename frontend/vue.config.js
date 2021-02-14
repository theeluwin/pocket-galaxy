const WEB_PORT = process.env.WEB_PORT
module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    port: WEB_PORT,
    host: '0.0.0.0',
    public: `0.0.0.0:${WEB_PORT}`,
    disableHostCheck: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
    }
  }
}
