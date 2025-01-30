<template>
  <div class="edit-graduate">
    <div class="header">
      <img src="@/assets/logo1.png" alt="Logo 1" class="logo">

    </div>
    <div class="form-box">
      <h1>Buscar y Editar Egresado</h1>
      <div class="search-box">
        <label for="cedula">Cédula</label>
        <input type="text" v-model="cedula" @keyup.enter="searchGraduate">
        <button @click="searchGraduate">Buscar</button>
      </div>
      <div v-if="egresado" class="edit-box">
        <h2>Editar Egresado</h2>
        <form @submit.prevent="editGraduate">

          <div class="form-row">
            <div class="input-group">
              <label for="nombre">Nombre</label>
              <input type="text" v-model="egresado.nombre">
            </div>
            <div class="input-group">
              <label for="cod_carrera">Código de Carrera</label>
              <input type="text" v-model="egresado.cod_carrera">
            </div>
          </div>

          <div class="form-row">
            <div class="input-group">
              <label for="cod_periodo">Código de Período</label>
              <input type="text" v-model="egresado.cod_periodo">
            </div>
            <div class="input-group">
              <label for="cedula">Cédula</label>
              <input type="text" v-model="egresado.cedula">
            </div>
          </div>

          <div class = "form-row">
            <div class="input-group">
              <label for="num_periodo">Número de Período</label>
              <input type="text" v-model="egresado.num_periodo">
            </div>
            <div class ="input-group">
              <label for="num_periodo">Número de Período</label>
              <input type="text" v-model="egresado.num_periodo">
            </div>
          </div>

          <div class = "form-row">
            <div class="input-group">
              <label for="aa">AA</label>
              <input type="text" v-model="egresado.aa">
            </div>
            <div class="input-group">
              <label for="pg">PG</label>
              <input type="text" v-model="egresado.pg">
            </div>
          </div>

          <div class = "form-row">
            <div class="input-group">
              <label for="pa">PA</label>
              <input type="text" v-model="egresado.pa">
            </div>
            <div class="input-group">
              <label for="rendimiento">Rendimiento</label>
              <input type="text" v-model="egresado.rendimiento">
            </div>
          </div>
  
          <div class = "form-row">
            <div class="input-group">
              <label for="fecha_grado">Fecha de Grado</label>
              <input type="date" v-model="egresado.fecha_grado">
            </div>          
          </div>
          <!-- Añade más campos según sea necesario -->
          <div class="buttons">
            <button type="button" @click="cancel">Cancelar</button>
            <button type="submit">Actualizar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditGraduate',
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
    async editGraduate() {
      const response = await fetch(`/api/editar/${this.egresado.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.egresado)
      });
      if (response.ok) {
        alert('Egresado editado con éxito');
        this.$router.push('/main');
      } else {
        alert('Error al editar egresado');
      }
    },
    cancel() {
      this.$router.push('/main');
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

.edit-graduate {
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

.header {
  position: absolute;
  top: 20px;
  width: 100%;
  display: flex;
  justify-content: flex-start; /* Mover el logo al lado izquierdo */
  padding-left: 20px; /* Añadir un poco de espacio a la izquierda */
}

.logo {
  height: 100px;
}

.form-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  color: #fff;
  padding: 40px 60px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 60%;
}

h1,
h2 {
  font-size: 3em; /* Texto más grande */
  margin-bottom: 20px;
}

.search-box,
.edit-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  padding: 20px;
  border-radius: 10px;
  text-align: left;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin-bottom: 20px;
  width: 80%; /* Ajustar ancho */
  max-width: 600px; /* Ancho máximo */
  margin-left: auto; /* Centrando */
  margin-right: auto; /* Centrando */
}

label {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  color: #fff;
}
input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  color: black;
}

input {
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.form-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.input-group {
  width: 48%; /* Ajustar ancho para dividir en dos columnas */
  text-align: left;
}

.buttons {
  display: flex;
  justify-content: center;
}

button {
  padding: 10px 20px;
  font-size: 16px;
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
