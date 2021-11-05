use Mojolicious::Lite -signatures;
use Mojo::JSON qw(decode_json encode_json to_json);

our @users = ();
# push @users, { fullname => 'blah blah blah' } for 1..10;

# map {print} @users;

get '/' => {
  text => 'perl with mojolicious'
};

# get '/api/users' => {
#   json => @users
# };

# put '/test' => sub ($c) {
#   $c->render(json => $chars);
# };

app->start;
