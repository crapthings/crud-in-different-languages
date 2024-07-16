#!/usr/bin/env perl

use strict;
use warnings;
use Mojolicious::Lite -signatures;
use Mojo::JSON qw(encode_json decode_json);
use Data::Faker;

my $faker = Data::Faker->new();

sub create_user {
    my $id = shift;
    return {
        _id => $id,
        username => $faker->username,
        email => $faker->email,
        fullname => $faker->name,
        avatarUrl => "https://i.pravatar.cc/150?u=" . $faker->email,
    };
}

my @users = map { create_user($_) } (1..10);

sub find_user_index {
    my ($user_id) = @_;
    for my $i (0..$#users) {
        return $i if $users[$i]->{_id} == $user_id;
    }
    return -1;
}

# GET /api/users
get '/api/users' => sub ($c) {
    $c->render(json => \@users);
};

# POST /api/users
post '/api/users' => sub ($c) {
    my $new_id = $users[-1]->{_id} + 1;
    my $user = create_user($new_id);
    push @users, $user;
    $c->render(json => $user);
};

# PUT /api/users/:_id
put '/api/users/:_id' => sub ($c) {
    my $user_id = $c->param('_id');
    my $user_index = find_user_index($user_id);

    if ($user_index >= 0) {
        my $updated_data = $c->req->json;
        $users[$user_index] = { %{$users[$user_index]}, %$updated_data };
        $c->render(json => $users[$user_index]);
    } else {
        $c->render(json => { error => 'User not found' }, status => 404);
    }
};

# DELETE /api/users/:_id
del '/api/users/:_id' => sub ($c) {
    my $user_id = $c->param('_id');
    my $user_index = find_user_index($user_id);

    if ($user_index >= 0) {
        splice @users, $user_index, 1;
        $c->render(json => { success => 1 });
    } else {
        $c->render(json => { error => 'User not found' }, status => 404);
    }
};

get '/' => sub ($c) {
    $c->render(text => 'Perl with Mojolicious');
};

app->start;
