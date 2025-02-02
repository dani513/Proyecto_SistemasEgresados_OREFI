<template>
  <div class="generate-letter">
    <div class="header">
      <img src="@/assets/logo2.png" alt="Logo 2" class="logo">
    </div>
    <div class="form-box">
      <h1>Generar Carta</h1>
      <div class="search-box">
        <label for="cedula">Cédula</label>
        <input type="text" v-model="cedula" @keyup.enter="searchGraduate">
        <button @click="searchGraduate">Buscar</button>
      </div>
      <div v-if="egresado">
        <h2>Información del Egresado</h2>
        <p><strong>Nombre:</strong> {{ egresado.nombre }}</p>
        <p><strong>Cédula:</strong> {{ egresado.cedula }}</p>
        <p><strong>Código de Carrera:</strong> {{ egresado.cod_carrera }}</p>
        <p><strong>Código de Período:</strong> {{ egresado.cod_periodo }}</p>
        <p><strong>Rendimiento:</strong> {{ egresado.rendimiento }}</p>
        <!-- Añade más campos según sea necesario -->
        <div class="buttons">
          <button @click="generateLetter('carta_tipo_1')">Puesto Pond_Apro</button>
          <button @click="generateLetter('carta_tipo_2')">Puesto Arit_ Apro</button>

          <button @click="generateLetter('carta_tipo_3')">Puesto Pond_ Apro_rend</button>
          <button @click="generateLetter('carta_tipo_4')">Puesto Arit_ Apro_rend</button>

          <button @click="generateLetter('carta_tipo_5')">Puesto Arit_gen_escuela</button>
          <button @click="generateLetter('carta_tipo_6')">Puesto Arit_gen_facultad</button>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GenerateLetter',
  data() {
    return {
      cedula: '',
      egresado: null
    }
  },
  methods: {
    async searchGraduate() {
      const response = await fetch(`/api/consultar?cedula=${this.cedula}`);
      if (response.ok) {
        const egresados = await response.json();
        if (egresados.length > 0) {
          this.egresado = egresados[0];
        } else {
          alert('No se encontró un egresado con esa cédula');
        }
      } else {
        alert('Error al buscar egresado');
      }
    },
    generateLetter(tipoCarta) {
      const url = `/api/generar-carta?cedula=${this.egresado.cedula}&tipoCarta=${tipoCarta}`;
      window.open(url, '_blank');
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

.generate-letter {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 70px); /* Altura ajustada para dejar espacio a la barra de tareas */
  padding-top: 70px; /* Añadir espacio arriba para la barra de tareas */
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

.form-box {
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

.search-box {
  margin-bottom: 20px;
}

label {
  font-size: 1.2em;
  margin-bottom: 5px;
  display: block;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-top: 5px;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  cursor: pointer;
  margin: 5px;
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
