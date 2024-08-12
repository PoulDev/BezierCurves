#include <SDL2/SDL.h>
#include <SDL2/SDL_events.h>
#include <SDL2/SDL_keycode.h>
#include <SDL2/SDL_mouse.h>
#include <SDL2/SDL_quit.h>
#include <SDL2/SDL_rect.h>
#include <SDL2/SDL_render.h>
#include <SDL2/SDL_stdinc.h>
#include <SDL2/SDL_timer.h>
#include <chrono>
#include <ctime>
#include <cmath>
#include <iostream>
#include <vector>


#define WIDTH 1080
#define HEIGHT 600
#define ZOOM 1
#define DEBUG false
#define DELAY 5

using namespace std;

float lerp_func(float a, float b, float t) {
    return (1 - t) * a + t * b;
}

float distance(SDL_Point point1, SDL_Point point2) {
    return sqrt(pow(point2.x - point1.x, 2) + pow(point2.y - point1.y, 2));
}

SDL_Point draw_bezier_lines(SDL_Renderer* renderer, vector<SDL_Point> connections, float t) {
    vector<SDL_Point> newConnections;
    
    if (connections.size() == 1)
        return connections[0];

    for (int i = 0; i < connections.size() - 1; i++) {
        float xlerp = lerp_func(connections[i].x, connections[i+1].x, t);
        float ylerp = lerp_func(connections[i].y, connections[i+1].y, t);

        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        SDL_RenderDrawLine(renderer, connections[i].x, connections[i].y, connections[i+1].x, connections[i+1].y);

        newConnections.push_back({(int)xlerp, (int)ylerp});
    }
    return draw_bezier_lines(renderer, newConnections, t);
}

int main() {
    bool running = true;
    SDL_Event e;
    SDL_Window* window;
    SDL_Renderer* renderer;
    vector<SDL_Point> punti_curva;
    float t = 0;
    Uint32 now, old, diff;
    bool done = false;
    int move_connection_index = -1;
    int mouseX, mouseY;

    cout << "Press enter to create a new point\n";
    cout << "Press backspace to delete the last point\n";
    cout << "Move the blu points with the mouse\n";

    vector<SDL_Point> connections = {
        {100, 100},
        {100, 500},
        {500, 500}, 
        {500, 100},
    };

    srand(time(NULL));

    SDL_Init(SDL_INIT_VIDEO);
    SDL_CreateWindowAndRenderer(WIDTH*ZOOM, HEIGHT*ZOOM, 0, &window, &renderer);
    SDL_RenderSetScale(renderer, ZOOM, ZOOM);

    old = SDL_GetTicks();
    auto start_time = chrono::system_clock::now();
    while (running) {
        if (t == 0)
            start_time = chrono::system_clock::now();

        SDL_SetRenderDrawColor(renderer, 0,0,0,255);
        SDL_RenderClear(renderer);

        if (!done)
            punti_curva.push_back(
                draw_bezier_lines(renderer, connections, t)
            );

        for (auto& punto : punti_curva) {
            SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
            SDL_RenderDrawPoint(renderer, punto.x, punto.y);
        }
        for (SDL_Point& connection : connections) {
            SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
            SDL_Rect rect = {connection.x-3, connection.y-3, 6, 6};
            SDL_RenderFillRect(renderer, &rect);
        }

        SDL_RenderPresent(renderer);

        if (!done) t += 0.01 / connections.size();
        if (t > 1) {
            t = 0;
            done = true;
            auto end_time = chrono::system_clock::now();
            chrono::duration<double> time_taken = end_time-start_time;

            cout << "Rendering Time: " << time_taken.count() << " secondi \n";
            cout << "Total Points: " << punti_curva.size() << '\n';
        }

        while(SDL_PollEvent(&e)) {
            switch (e.type) {
                case SDL_QUIT: {
                    SDL_Quit();
                    exit(0);
                    break;
                } case SDL_KEYUP: {
                    if (e.key.keysym.sym == SDLK_RETURN) {
                        SDL_GetMouseState(&mouseX, &mouseY);
                        connections.push_back({mouseX, mouseY});
                        punti_curva.clear();

                        done = false;
                        t = 0;
                    } else if (e.key.keysym.sym == SDLK_BACKSPACE && connections.size() > 1) {
                        connections.pop_back();
                        done = false;
                        t = 0;
                        punti_curva.clear();
                    }

                    break;
                } case SDL_MOUSEMOTION: {
                    if (move_connection_index >= 0) {
                        connections[move_connection_index].x = e.motion.x;
                        connections[move_connection_index].y = e.motion.y;
                    }
                    break;
                } case SDL_MOUSEBUTTONDOWN: {
                    for (int i = 0; i < connections.size(); i++) {
                        SDL_Point connection = connections[i];
                        SDL_GetMouseState(&mouseX, &mouseY);
                        if (distance({mouseX, mouseY}, connection) < 12) {
                            move_connection_index = i;
                        }
                    }
                    break;
                } case SDL_MOUSEBUTTONUP: {
                    if (move_connection_index >= 0) {
                        move_connection_index = -1;
                        punti_curva.clear();
                        done = false;
                        t = 0;
                    }
                    break;
                }
            }
        }

        now = SDL_GetTicks();
        diff = now - old;
        if (diff >= 0 && diff < DELAY)
            SDL_Delay(DELAY - diff);
        old = now;
    }
}

