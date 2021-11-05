use Data::Faker;

my $faker = Data::Faker -> new();

our $count = 0;
our @users = ();

push @users, { fullname => $faker -> name } for 1..10;

for my $user (@users) {
  $user -> { _id } = $count;
  $count++;
  print $_;
  print $user -> { _id } . ". " . $user -> { fullname } . "\n";
};
