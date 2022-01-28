// let game = new BoggleGame();

class BoggleGame {
    constructor() {
        this.secs = 60;
        this.timer = setInterval(this.countDown.bind(this), 1000);
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.msgs = {
            notWord: ' is not a word.',
            notOnBoard: ' is not on the board.',
            wordOk: ' is on board!',
            dupe: ' has already been played.',
            highScore: ' NEW HIGH SCORE!'
        };
        $("#get-guess").on("submit", this.handleGuess.bind(this));
        $('#ok').hide();
        $('#no').hide();
        $('#game-over').hide();

    }

    async countDown() {
        this.secs -= 1
        this.showTimer();
        if(this.secs === 0) {
            clearInterval(this.timer);
            this.gameOver();
            await this.postScore();
        }
    } 

    showTimer() {
        $('#timer').text(this.secs);
    }

    async handleGuess(evt) {
        evt.preventDefault();
        const $guess = $('#guess').val();

        if(!this.words.has($guess)) {
            this.words.add($guess);
            this.checkWord($guess);
        }
        else {
            $('#ok').hide();
            $('#no').show();
            $('#no').text($guess + this.msgs.dupe);
        }
        $('#get-guess').trigger('reset');
    }

    async checkWord(guess) {
        const res = await axios.get('/check-word', {params: {guess: guess}});
        this.handleResult(res.data.result, guess);
    }

    async handleResult(res, word) {
        const $msg = $(".messages");
        if(res === 'ok') {
            $('#ok').show();
            $('#no').hide()
            this.score += word.length;
            $('#ok').text(word + this.msgs.wordOk + ` + ${word.length} points!`);
            this.showScore();
            this.showWord(word);
        }
        if(res === 'not-word') {
            $('#no').show();
            $('#ok').hide();
            $('#no').text(word + this.msgs.notWord);
        }
        if(res === 'not-on-board') {
            $('#no').show();
            $('#ok').hide();
            $('#no').text(word + this.msgs.notOnBoard);
        }
    }

    async showWord(word) {
        // $('.hidden').show()
        const id = this.words.length;
        const showWord = $(`<span id=${id}>${word}</span>`);
        $('#played-words').append(showWord);
    }

    async postScore() {
        const res = await axios.post('/post-score', {score: this.score});
    
        console.log('response', res.data);
        if(res.data.highScore === true) {
            $('#ok').show();
            $('#ok').text(this.score + this.msgs.highScore);
            $('#high-score').text(this.score);
        }
    }
    
    showScore() {
        $('#score').text(this.score);
    }

    gameOver() {
        $("#get-guess").off("submit");
        $('#game-over').show()
        $('button').text('Replay?')
    }
}

let game = new BoggleGame();

