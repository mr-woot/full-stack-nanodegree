module.exports = function(grunt) {

    /*Loading our config*/
    var config = grunt.file.readYAML('Gruntconfig.yml');

    /*Load Grunt Tasks*/
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        sass: {
            dist: {
                src: config.scssDir + 'style.scss',
                dest: config.cssDir + 'style.css'
            }
        },
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
        'sass',
        'concat',
        'jshint'
    ]);
};
