<template>
  <div class="container">
    <link rel="stylesheet">

    <!--    左边的部分-->
    <div class="left-container">
      <h3>您想比较的图——您可以选择手动上传</h3>
      <div>
        <el-upload list-type="picture-card" auto-upload="auto-upload">
          <i class="el-icon-plus"></i>
        </el-upload>
        <br>
        <div>
          <h3>或者点此
            <el-button type="primary"><i class="el-icon-camera"></i>拍照</el-button>
          </h3>

        </div>
        <img :src="imgUrl" alt="图" v-if="imgUrl!==''">
      </div>

    </div>

    <!--    右边的部分-->
    <div class="right-container">
      <el-tag
          key="pic2"
          type="success"
          effect="dark">
        图片二
      </el-tag>
      <el-upload
          class="upload-demo"
          drag
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传jpg/png文件</div>
      </el-upload>
    </div>

  </div>
</template>

<script>


export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      imgUrl: "../assets/upload1/alm9x-kj0rm.jpg"
    }
  },

  methods: {}

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.container {
  display: flex;
  height: 100vh;

}

.left-container,
.right-container {
  flex: 1;
  border: 1px solid #ccc;
}


</style>
