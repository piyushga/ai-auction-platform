CREATE TABLE players (
    player_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    age INT,
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    role VARCHAR(30),
    current_ipl_team VARCHAR(100)
);

CREATE TABLE t20i_records (
    player_id INT PRIMARY KEY,
    matches INT NOT NULL,
    innings INT NOT NULL,
    runs INT NOT NULL,
    batting_average DECIMAL(5,2),
    strike_rate DECIMAL(5,2),
    highest_score INT,
    fours INT,
    sixes INT,
    fifties INT,
    hundreds INT,
    wickets INT,
    bowling_average DECIMAL(5,2),
    economy DECIMAL(4,2),
    best_bowling VARCHAR(10),
    five_wicket_hauls INT,
    catches INT,
    CONSTRAINT fk_t20i_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
);

CREATE TABLE ipl_career_stats (
    player_id INT PRIMARY KEY,
    matches INT NOT NULL,
    innings INT NOT NULL,
    runs INT NOT NULL,
    batting_average DECIMAL(5,2),
    strike_rate DECIMAL(5,2),
    highest_score INT,
    fours INT,
    sixes INT,
    fifties INT,
    hundreds INT,
    wickets INT,
    bowling_average DECIMAL(5,2),
    economy DECIMAL(4,2),
    best_bowling VARCHAR(10),
    five_wicket_hauls INT,
    catches INT,
    CONSTRAINT fk_ipl_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
);

CREATE TABLE auction_history (
    id INT PRIMARY KEY,
    player_id INT NOT NULL,
    auction_year INT NOT NULL,
    team VARCHAR(100) NOT NULL,
    base_price BIGINT NOT NULL,
    sold_price BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_auction_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
);

CREATE TABLE special_stats (
    id INT PRIMARY KEY,
    player_id INT NOT NULL,
    stat_name VARCHAR(100) NOT NULL,
    stat_value VARCHAR(100) NOT NULL,
    format VARCHAR(20) NOT NULL,
    season_year INT NOT NULL,
    CONSTRAINT fk_special_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS player_embeddings (
    id SERIAL PRIMARY KEY,

    player_id INT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,

    player_name VARCHAR(100) NOT NULL,

    description TEXT NOT NULL,

    embedding vector(1536) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);