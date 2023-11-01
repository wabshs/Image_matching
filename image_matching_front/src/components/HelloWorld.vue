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
        <img :src="imgUrl" alt="图" v-if="leftImgExist===true" class="leftImg">
      </div>

      <div class="sakana"></div>

    </div>

    <!--    右边的部分-->
    <div class="right-container">
      <h3>原图——您可以选择手动上传</h3>
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
        <img :src="imgUrl" alt="图" v-if="leftImgExist===true" class="leftImg">
      </div>
    </div>

  </div>
</template>

<script>
import 'sakana-widget/lib/index.css';
import SakanaWidget from 'sakana-widget';


export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      imgUrl: require(),
      leftImgExist: false,
      rightImgExist: false,
    }
  },

  mounted() {
    new SakanaWidget().mount('.sakana');
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.container {
  display: flex;
  height: 100vh;

}

.leftImg {
  max-width: 100%;
  height: auto;
  width: 100%;
}

.left-container,
.right-container {
  flex: 1;
  border: 1px solid #ccc;
}




</style>
