<template>
  <div class="welcome-page">
    <div class="header">
      <img src="@/assets/logo1.png" alt="Logo 1" class="logo-left">
      <img src="@/assets/logo2.png" alt="Logo 2" class="logo-right">
    </div>
    <div class="welcome-box">
      <h1>Bienvenido a la Plataforma de Egresados</h1>
      <button @click="goToLogin">Iniciar Sesión</button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'WelcomePage',
  methods: {
    goToLogin() {
      this.$router.push('/login');
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

.welcome-page {
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
  justify-content: space-between;
  padding: 0 50px;
}

.logo-left,
.logo-right {
  height: 100px;
}

.welcome-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  color: #fff;
  padding: 40px 30px; /* Reducir el padding para hacerla más angosta */
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 40%; /* Reducir el ancho */
}

h1 {
  font-size: 2.5em; /* Texto más grande */
  margin-bottom: 20px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  cursor: pointer;
  color: #fff;
  background-color: #000066;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
}

button:hover {
  background-color: #333399;
  transform: translateY(-4px);
}
</style>
