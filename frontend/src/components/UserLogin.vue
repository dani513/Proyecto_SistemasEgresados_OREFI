<template>
  <div class="user-login">
    <div class="header">
      <img src="@/assets/logo1.png" alt="Logo 1" class="logo">
    </div>
    <div class="login-box">
      <h1>Iniciar Sesión</h1>
      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">Usuario</label>
          <input type="text" v-model="username" required>
        </div>
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input type="password" v-model="password" required>
        </div>
        <button type="submit">Iniciar sesión</button>
      </form>
    </div>
  </div>
</template>


<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: this.username, password: this.password })
      });
      if (response.ok) {
        this.$router.push('/main');
      } else {
        alert('Usuario o contraseña incorrectos');
      }
    }
  }
}
</script>


<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background: url('@/assets/background.jpg') no-repeat center center fixed; /* Imagen de fondo */
  background-size: cover; /* Asegura que la imagen cubra toda la pantalla */
}

.user-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #fff;
  position: relative;
}

.header {
  position: absolute;
  top: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.logo {
  height: 100px;
}

.login-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  color: #fff;
  padding: 40px 60px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

h1 {
  font-size: 3em; /* Texto más grande */
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  font-size: 1.2em;
  margin-bottom: 5px;
  display: block;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-top: 5px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  cursor: pointer;
  color: #000066;
  background: #fff;
  border: none;
  border-radius: 5px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s, transform 0.3s;
  margin-top: 20px;
}

button:hover {
  background-color: #e0e0e0;
  transform: translateY(-6px);
}
</style>
