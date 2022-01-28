const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;

export default {
  data () {
    return {
     
      formRulesMixin_minLengthSix: [val => val.length >= 6 || this.$t('validation.minCharacterLength').replace('{NUMBER}', '6')],
      required: [val => !!val || 'Este campo no puede estar en blanco'],
      email:[val => emailPattern.test(val) || 'Correo no valido']

    }
  }
}
