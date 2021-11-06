use Mojolicious::Lite -signatures;
use Data::Faker;

my $faker = Data::Faker -> new();

our $count = 0;
our @users = ();

push @users, { fullname => $faker -> name } for 1..10;

for my $user (@users) {
  $user -> { _id } = $count;
  $count++;
};


get '/' => text => 'perl with mojolicious';

app->start;
