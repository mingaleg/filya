#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

#define X_dim 41
#define Y_dim 45


vector<vector<short> > Pole(X_dim);
vector<vector<bool> > used(X_dim);
vector<pair<int, int> > cnt_col(6);

void Input()
{
	for (int i = 0; i < X_dim; i++)
	{
		for (int q = 0; q < Y_dim; q++)
		{
			cin >> Pole[i][q];
		}
	}
}

int dx[4] = {-1, 0, 0, 1};
int dy[4] = {0, 1, -1, 0};

void dfs(int x, int y)
{
	used[x][y] = true;
	for (int i = 0; i < 4; i++)
	{
		if (x + dx[i] < 0 || x + dx[i] >= X_dim || y + dy[i] < 0 || y + dy[i] >= Y_dim)
			continue;
		if (!used[x + dx[i]][y + dy[i]])
		{
			if (Pole[x + dx[i]][y + dy[i]] == Pole[x][y])
				dfs(x + dx[i], y + dy[i]);
			else
			{
				cnt_col[Pole[x + dx[i]][y + dy[i]] - 1].first++;
				used[x + dx[i]][y + dy[i]] = true;
			}
		}
	}
}

int main()
{
	for (int i = 0; i < X_dim; i++)
	{
		Pole[i].assign(Y_dim, 0);
		used[i].assign(Y_dim, false);
	}
	Input();
	for (int i = 0; i < 6; i++)
	{
		cnt_col[i].first = 0;
		cnt_col[i].second = i + 1;
	}
	dfs(0, 0);
	sort(cnt_col.begin(), cnt_col.end());
	reverse(cnt_col.begin(), cnt_col.end());
	for (int i = 0; i < 6; i++)
	{
		if (cnt_col[i].second != Pole[X_dim - 1][Y_dim - 1] && cnt_col[i].second != Pole[0][0])
		{
			cout << cnt_col[i].second << endl;
			break;
		}
	}
	return 0;
}
