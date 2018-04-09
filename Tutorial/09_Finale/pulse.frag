#version 330

in vec4 pos_out;
in vec4 mv_pos;
in vec4 colour_out;
in float time_out;

out vec4 fragColour;

void main()
{
    
    vec3 normal = cross(dFdx(mv_pos.xyz), dFdy(mv_pos.xyz));
    float m = dot(normalize(mv_pos.xyz), normalize(normal));
    float n = dot(dFdx(mv_pos.xyz), dFdy(mv_pos.xyz));
    vec3 e = normalize(abs((cross( pos_out.xyz, normal))));
    vec3 fc = 1 - e;
    if(m > -0.975 - 0.025 * sin(time_out * 50.0))
    {
        fc = e;
    }

    if(n <  0.0001 * sin(time_out * 5.0))
    {
        fc = mix(vec3(sin(time_out * 100.0) * 0.5 + 0.5), e, 0.3);
    }

    fragColour = vec4(fc, 1.0);
}