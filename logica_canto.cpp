#include <bits/stdc++.h>

#define endl '\n'

using namespace std;

int ehrua[5][14];
int m[2][11];
pair<int,int> moves[] = {{0,0}, {0,-1}, {-1,0}, {-1,-1}};

void solve(){
    int n; cin >> n;
    for(int i = 1; i < 3; i++) for(int j = 1; j < 12; j++){
        ehrua[i][j] = 1;
    }
    while(n != -1){
        int linha;
        if(n % 3 == 0){
            linha = 1;
        } else if (n % 3 == 1){
            linha = 3;
        } else {
            linha = 2;
        }
        int coluna = (n-1)/3+1;
        cout << linha << ' ' << coluna << endl;
        for(int i = 0; i < 2; i++){
            for(int j = 0; j < 11; j++){
                m[i][j]++;
            }
        }
        for(int i = 0; i < 4; i++){
            auto [ii,jj] = moves[i];
            if(ehrua[linha+ii][coluna+jj]){
                m[linha-1+ii][coluna-1+jj] = 0;       
            }
        }
        for(int i = 0; i < 2; i++){
            for(int j = 0; j < 11; j++){
                cout << m[i][j] << ' ';
            }
            cout << endl;
        }
        cin >> n;
    }
}

int main(){
    solve();
    return 0;
}
