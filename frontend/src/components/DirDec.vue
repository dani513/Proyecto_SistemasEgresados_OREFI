<template>
  <div class="dir-dec">
    <div class="header">
      <img src="@/assets/logo2.png" alt="Logo 2" class="logo">
    </div>
    <div class="form-box">
      <h1>Director de OREFI y Decano</h1>
      <form @submit.prevent="updateInfo" v-if="canEdit">
        <div class="input-group">
          <label for="director">Director de OREFI</label>
          <input type="text" v-model="director" placeholder="Nombre del Director de OREFI">
        </div>
        <div class="input-group">
          <label for="decano">Decano</label>
          <input type="text" v-model="decano" placeholder="Nombre del Decano">
        </div>
        <div class="buttons">
          <button type="button" @click="cancel">Cancelar</button>
          <button type="submit">Actualizar</button>
        </div>
      </form>
      <div v-else>
        <p>Director de OREFI: {{ director }}</p>
        <p>Decano: {{ decano }}</p>
        <p>No tienes permiso para editar esta información.</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'DirDec',
  data() {
    return {
      director: '',
      decano: '',
      canEdit: false
    }
  },
  created() {
    this.fetchInfo();
  },
  methods: {
    async fetchInfo() {
      const response = await fetch('/api/informacion');
      if (response.ok) {
        const data = await response.json();
        this.director = data.director;
        this.decano = data.decano;
        this.canEdit = data.can_edit;
      } else {
        alert('Error al consultar la información');
      }
    },
    async updateInfo() {
      if (!this.canEdit) {
        alert('No tienes permiso para actualizar esta información');
        return;
      }
      const response = await fetch('/api/actualizar_informacion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          director: this.director,
          decano: this.decano
        })
      });
      if (response.ok) {
        alert('Información actualizada con éxito');
        this.$router.push('/main');
      } else {
        alert('Error al actualizar la información');
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

.dir-dec {
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

.input-group {
  margin-bottom: 15px;
  text-align: left;
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
