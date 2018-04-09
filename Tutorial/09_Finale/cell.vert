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
    pos_out = model * position;//+ vec4(cos(position.x + time_in * 50.0), sin(position.y + time_in * 50.0), 0.0, 0.0);
    mv_pos = view * pos_out;
    //mv_pos.x = (sin(pos_out.y + time_in * 30.0) - cos(pos_out.z + time_in * 50.0)) ;
    mv_pos.y = (sin(pos_out.z + time_in * 20.0) + cos(pos_out.x + time_in * 25.0));
    //mv_pos.z = (sin(pos_out.y + time_in * 50.0) + cos(pos_out.x+ time_in * 50.0));
    gl_Position = proj * mv_pos;
    gl_Position.y += (sin(time_in * 42.0) + cos(pos_out.z + time_in * 3.0)) - 40.0;
    colour_out = colour_in;
    time_out = time_in;
}