module.exports = function(grunt) {

    /*Loading our config*/
    var config = grunt.file.readYAML('Gruntconfig.yml');

    /*Load Grunt Tasks*/
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        concat: {
            dist: {
                src: config.jsSrcDir + '*.js',
                dest: config.jsConcatDir + 'scripts.js',
            }
        },
        jshint: {
            options: {
                "eqeqeq": true
            },
            all: [
                'Gruntfile.js',
                config.jsSrcDir + "*.js"
            ]
        }
    });

    grunt.registerTask('default', [
        'jshint',
        'concat'
    ]);
};
