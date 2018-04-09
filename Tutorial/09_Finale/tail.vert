#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;
uniform float time_in;

in vec4 position;
in vec4 colour_in;

out vec4 pos_out;
out vec4 mv_pos;
out vec4 colour_out;
out float time_out;

void main()
{
    pos_out = model * position;
    mv_pos = view * model * position;
    gl_Position = proj * mv_pos;
    colour_out = colour_in;
    time_out = time_in;
}