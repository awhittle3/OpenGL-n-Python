#version 330

in vec4 pos_out;
in vec4 mv_pos;
in vec4 colour_out;
in float time_out;

out vec4 fragColour;

void main()
{
    fragColour = colour_out;
}